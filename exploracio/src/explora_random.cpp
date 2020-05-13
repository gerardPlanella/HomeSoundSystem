#include "explora_random.h"

ExploraRandom::ExploraRandom(ros::NodeHandle& nh) :
    nh_(nh),
    robot_status_(1),
    num_celles_(0),
    num_goals_enviats_(0),
    num_goals_ok_(0),
    distancia_recorreguda_(0),
    inici_exploracio_(ros::Time::now()),
    celles_explorades_(0),
    exploracio_acabada_(false),
    action_move_base_("move_base",true)
{

    nh_.param<int>("tamany_min_frontera", min_frontier_size_, 5);
    map_sub_             = nh_.subscribe("/map", 1, &ExploraRandom::mapCallback,this);
    fronteres_sub_       = nh_.subscribe("/fronteres", 1, &ExploraRandom::fronteresCallback,this);

    goal_marker_pub_     = nh_.advertise<visualization_msgs::Marker>("goal_marker", 1);

    get_plan_client_     = nh_.serviceClient<nav_msgs::GetPlan>("/move_base/NavfnROS/make_plan");
}

void ExploraRandom::mapCallback(const nav_msgs::OccupancyGrid::ConstPtr& msg)
{
    map_=*msg;
}

void ExploraRandom::fronteresCallback(const exploracio::Fronteres::ConstPtr& msg)
{
    fronteres_=*msg;
}

bool ExploraRandom::replanifica()
{
  bool replan = false;

  //EXEMPLE: replanifica quan el robot hagi arribat
  if(robot_status_!=0)
    replan = true;

  return replan;
}

geometry_msgs::Pose ExploraRandom::decideixGoal()
{
  geometry_msgs::Pose g;
  double length;

  //EXEMPLE: Genera destins random fins que sigui goal valid
  do
  {
    g = generaRandomPoseAlVoltant(3.0, robot_pose_);
  }
  while(!esGoalValid(g.position, length ));

  return g;
}
void ExploraRandom::treballa()
{
    if(actualitzaPosicioRobot())
    {
      if(replanifica())
      {
        target_goal_ = decideixGoal();
        moveRobot(target_goal_);
      }
    }
    else
      ROS_WARN("Couldn't get robot position!");

    // FINAL
    if (exploracio_acabada_)
        acaba();
}

void ExploraRandom::acaba()
{
    double t = (ros::Time::now() - inici_exploracio_).toSec();
    int t_min = int(t)/60;
    int t_sec = int(t)%60;

    ROS_INFO_ONCE("EXPLORACIÓ ACABADA");
    ROS_INFO_ONCE("--- Enviats %d goals (arribats %d).", num_goals_enviats_, num_goals_ok_);
    ROS_INFO_ONCE("--- Distància recorreguda %.2f m.", distancia_recorreguda_);

    ROS_INFO_ONCE("--- Duració %2.2i:%2.2i minutes", t_min, t_sec);
    ROS_INFO_ONCE("--- Explorat %.2f m^2 (%d celles).", celles_explorades_*map_.info.resolution*map_.info.resolution, celles_explorades_);
    ROS_INFO_ONCE("Si vols salvar el mapa, recorda fer: $rosrun map_server map_saver -f my_map_name");

    ros::shutdown();
}

///// FUNCIONS AUXILIARS //////////////////////////////////////////////////////////////////////
geometry_msgs::Pose ExploraRandom::generaRandomPoseAlVoltant(float radius, const geometry_msgs::Pose& referencia)
{
  geometry_msgs::Pose goal_pose;

  srand((unsigned)time(NULL));
  if (radius <= 0)
  {
      ROS_WARN("getRandomPose: radius must be > 0. Changed to 1");
      radius = 1;
  }

  // dona una pose entre +-radius al voltant de referencia
  float rand_yaw = 2*M_PI * (rand()%100)/100.0;
  float rand_r = radius*(rand()%100)/100.0;

  goal_pose.position.x = referencia.position.x + rand_r * cos(rand_yaw);
  goal_pose.position.y = referencia.position.y + rand_r * sin(rand_yaw);
  goal_pose.orientation = tf::createQuaternionMsgFromYaw(tf::getYaw(referencia.orientation) + rand_yaw);

  return goal_pose;
}

bool ExploraRandom::esGoalValid(const geometry_msgs::Point & point, double & path_length)
{
  bool valid=false;
  nav_msgs::GetPlan get_plan_srv;
  get_plan_srv.request.start.header.stamp = ros::Time::now();
  get_plan_srv.request.start.header.frame_id = "map";
  get_plan_srv.request.start.pose = robot_pose_;

  get_plan_srv.request.goal.header.stamp = ros::Time::now();
  get_plan_srv.request.goal.header.frame_id = "map";
  get_plan_srv.request.goal.pose.position.x = point.x;
  get_plan_srv.request.goal.pose.position.y = point.y;
  get_plan_srv.request.goal.pose.orientation.w = 1.0;
  if (get_plan_client_.call(get_plan_srv))
  {
    if(get_plan_srv.response.plan.poses.size()!=0)
    {
      path_length = calculaLongitudPlan(get_plan_srv.response.plan.poses);
      ROS_INFO("path length %f", path_length);
      valid=true;
    }
  }
  else
    ROS_ERROR("Failed to call service get_plan");

  return valid;
}

double ExploraRandom::calculaLongitudPlan(std::vector<geometry_msgs::PoseStamped> poses)
{
  double length=0.0;
  if(poses.size()>=1)
  {
    for(unsigned int i=1; i<poses.size(); i++)
    {
      double x1 = poses[i-1].pose.position.x;
      double y1 = poses[i-1].pose.position.y;
      double x2 = poses[i].pose.position.x;
      double y2 = poses[i].pose.position.y;
      double d = sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2));
      length +=d;
    }
  }
  return length;
}

// FUNCIONS DE NAVEGACIÓ ////////////////////////////////////////////////////////////////////////////////////////
//moveRobot: envia un goal al robot
bool ExploraRandom::moveRobot(const geometry_msgs::Pose& goal_pose)
{
  //espera action server
  if(!action_move_base_.waitForServer(ros::Duration(5.0)))
  {
    ROS_INFO("moveRobot: Waiting for the move_base action server to come up");
    return false;
  }

  // escriu the frame_id i stamp
  move_base_msgs::MoveBaseGoal goal;
  goal.target_pose.header.frame_id = "/map";
  goal.target_pose.header.stamp = ros::Time::now();
  goal.target_pose.pose = goal_pose;

  num_goals_enviats_++;
  ROS_INFO("moveRobot: Enviant Goal #%d: x=%4.2f, y=%4.2f, yaw=%4.2f al frame_id=%s",
           num_goals_enviats_,
           goal.target_pose.pose.position.x,
           goal.target_pose.pose.position.y,
           tf::getYaw(goal.target_pose.pose.orientation) ,
           goal.target_pose.header.frame_id.c_str());

  ros::Duration t = ros::Time::now() - inici_exploracio_;
  int elapsed_time_minutes = int(t.toSec())/60;
  int elapsed_time_seconds = int(t.toSec())%60;
  ROS_INFO("Status de l'exploració: Enviats %d goals (assolits %d). Distància recorreguda %.2f m. Han passat %2.2i:%2.2i min. Explorats %.2f m^2 (%d cel·les)",
           num_goals_enviats_,
           num_goals_ok_,
           distancia_recorreguda_,
           elapsed_time_minutes, elapsed_time_seconds,
           celles_explorades_*map_.info.resolution*map_.info.resolution,
           celles_explorades_);

  action_move_base_.sendGoal(goal,
                             boost::bind(&ExploraRandom::move_baseDone, this, _1, _2),
                             actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction>::SimpleActiveCallback(),
                             actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction>::SimpleFeedbackCallback());
  robot_status_=0; //movent-se
  return true;
}

//move_baseDone: es crida quan el robot assoleix un goal o es cancela per alguna raó
void ExploraRandom::move_baseDone(const actionlib::SimpleClientGoalState& state,  const move_base_msgs::MoveBaseResultConstPtr& result)
{
  //ROS_INFO("move_baseDone");
  if(state==actionlib::SimpleClientGoalState::SUCCEEDED)
  {
    robot_status_=1; //èxit
    num_goals_ok_++;
  }
  else
    robot_status_=2; //error
}

// Calcula la posició actual a través de TF
bool ExploraRandom::actualitzaPosicioRobot()
{
  static bool first=true;
  tf::StampedTransform transform;
  ros::Time target_time = ros::Time(0); //ros::Time::now();
  std::string source_frame = "/map";
  std::string target_frame = "/base_footprint";
  try
  {
    if(listener_.waitForTransform(source_frame, target_frame, target_time, ros::Duration(5.0)))
        listener_.lookupTransform(source_frame, target_frame, target_time, transform);
    else
    {
      ROS_ERROR("refreshRobotPosition: no transform between frames %s and %s", source_frame.c_str(), target_frame.c_str());
      return false;
    }
  }
  catch(tf::TransformException ex)
  {
    ROS_ERROR("%s",ex.what());
    return false;
  }
  robot_pose_.position.x = transform.getOrigin().x();
  robot_pose_.position.y = transform.getOrigin().y();
  robot_pose_.position.z = 0.0;
  robot_pose_.orientation = tf::createQuaternionMsgFromYaw(tf::getYaw(transform.getRotation()));
  //ROS_INFO("base_link|map: x:%fm y:%fm th:%fº", robot_pose_.position.x, robot_pose_.position.y, tf::getYaw(robot_pose_.orientation));

  if(first)
  {
    prev_robot_pose_=robot_pose_;
    first=false;
  }

  float dist_incr=std::sqrt(std::pow(prev_robot_pose_.position.x-robot_pose_.position.x,2)+std::pow(prev_robot_pose_.position.y-robot_pose_.position.y,2));
  float angle_incr=fabs(tf::getYaw(prev_robot_pose_.orientation)-tf::getYaw(robot_pose_.orientation));
  float d=0.115; //half of the distance between wheels
  distancia_recorreguda_ += (fabs(dist_incr+d*angle_incr)+fabs(dist_incr-d*angle_incr))/2.0f;

  prev_robot_pose_=robot_pose_;
  return true;
}

////// MAIN ////////////////////////////////////////////////////////////////////////////
int main(int argc, char **argv)
{
    ros::init(argc, argv, "explora_random_node");
    ros::NodeHandle nh("~");
    ExploraRandom node_explora(nh);
    ros::Rate loop_rate(10);

    while (ros::ok())
    {
        ros::spinOnce();
        loop_rate.sleep();

        node_explora.treballa();
    }
    return 0;
}

