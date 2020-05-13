#include "../include/explora_fronteres.h"

ExploraFronteraMajor::ExploraFronteraMajor(ros::NodeHandle& nh) :
    nh_(nh),
    robot_status_(1),
    num_celles_(0),
    num_goals_enviats_(0),
    num_goals_ok_(0),
    distancia_recorreguda_(0),
    inici_exploracio_(ros::Time::now()),
    celles_explorades_(0),
    exploracio_acabada_(false),
    exploracio_iniciada_(false),
    action_move_base_("move_base",true)
{

    map_sub_             = nh_.subscribe("/map", 1, &ExploraFronteraMajor::mapCallback,this);
    fronteres_sub_       = nh_.subscribe("/fronteres", 1, &ExploraFronteraMajor::fronteresCallback,this);

    goal_marker_pub_     = nh_.advertise<visualization_msgs::Marker>("goal_marker", 1);

    get_plan_client_     = nh_.serviceClient<nav_msgs::GetPlan>("/move_base/NavfnROS/make_plan");

    srand((unsigned)time(NULL));
}

void ExploraFronteraMajor::mapCallback(const nav_msgs::OccupancyGrid::ConstPtr& msg)
{
    map_=*msg;

    // calcula cel·les explorades
    celles_explorades_ = 0;
    for(int i = 0; i < map_.data.size(); ++i)
    {
        if(map_.data[i] != -1)
        {
            celles_explorades_++;
        }
    }
}

void ExploraFronteraMajor::fronteresCallback(const exploracio::Fronteres::ConstPtr& msg)
{
    fronteres_msg_=*msg;

    // Fins que no hi ha cap missatge de fronteres, no comença l'exploració
    exploracio_iniciada_ = true;

    // Si no hi ha noves fronteres, finalitza l'exploració
    if (fronteres_msg_.fronteres.empty())
        exploracio_acabada_ = true;

//    printf("============== Nou missatge Fronteres rebut! ==============\n");
//    printf("stamp: %i.%i | frame_id: %s | seq: %i\n", fronteres_msg_.header.stamp.sec, fronteres_msg_.header.stamp.nsec, fronteres_msg_.header.frame_id.c_str(), fronteres_msg_.header.seq);
//    printf("Fronteres: %lu\n", fronteres_msg_.fronteres.size());
//    for (int i = 0; i < fronteres_msg_.fronteres.size(); i++)
//    {
//        printf("\tfrontera %i:\n",i);
//        printf("\t\tid %i\n",fronteres_msg_.fronteres[i].id);
//        printf("\t\tsize %i\n",fronteres_msg_.fronteres[i].size);
//        printf("\t\tcentre_punt %f, %f, %f\n",fronteres_msg_.fronteres[i].centre_punt.x,fronteres_msg_.fronteres[i].centre_punt.y,fronteres_msg_.fronteres[i].centre_punt.z);
//        //printf("\t\tcentre_cella %i\n",fronteres_msg_.fronteres[i].centre_cella);
//        printf("\t\tcentre_lliure_punt %f, %f, %f\n",fronteres_msg_.fronteres[i].centre_lliure_punt.x,fronteres_msg_.fronteres[i].centre_lliure_punt.y,fronteres_msg_.fronteres[i].centre_lliure_punt.z);
//        //printf("\t\tcentre_lliure_cella %i\n",fronteres_msg_.fronteres[i].centre_lliure_cella);
//        //printf("\t\tcelles_punts:\n");
//        //for (int j = 0; j<fronteres_msg_.fronteres[i].celles_punts.size(); j++)
//        //{
//        //    printf("\t\t\t%f, %f, %f\n",fronteres_msg_.fronteres[i].celles_punts[j].x,fronteres_msg_.fronteres[i].celles_punts[j].y,fronteres_msg_.fronteres[i].celles_punts[j].z);
//        //}
//        //printf("\t\tcelles_celles:\n");
//        //for (int j = 0; j<fronteres_msg_.fronteres[i].celles_punts.size(); j++)
//        //{
//        //    printf("\t\t\t%i\n",fronteres_msg_.fronteres[i].celles_celles[j]);
//        //}
//    }
}

bool ExploraFronteraMajor::replanifica()
{
  bool replan = false;

  //EXEMPLE: replanifica quan el robot hagi arribat
  if(robot_status_!=0)
    replan = true;

  return replan;
}

geometry_msgs::Pose ExploraFronteraMajor::decideixGoal()
{
  geometry_msgs::Pose g;
  double longitud;

  // Repassem les fronteres per trobar la més gran
  int i_max = 0;
  for (int i = 1; i < fronteres_msg_.fronteres.size(); i++)
  {
      // guardem i si la frontera i és més gran que la guardada a i_max
      if (fronteres_msg_.fronteres[i].size > fronteres_msg_.fronteres[i_max].size)
      {
          i_max = i;
      }
  }
  // Guardem al goal la posició del centre lliure de la frontera i la orientació actual que el robot (per exemple)
  g.position = fronteres_msg_.fronteres[i_max].centre_lliure_punt;
  g.orientation = robot_pose_.orientation;

  // Si el centre_lliure_punt de la frontera més gran no és un goal vàlid, generem un goal random al voltant
  // Anirem augmentant el radi fins que trobem un goal vàlid
  double radi = 1.0;
  while (!esGoalValid(g.position, longitud))
  {
      printf("!!! Goal no valid (frontera id: %i). Generant goal random amb radi %f...\n",fronteres_msg_.fronteres[i_max].id,radi);
      g.position = fronteres_msg_.fronteres[i_max].centre_lliure_punt;
      g.orientation = robot_pose_.orientation;
      g = generaRandomPoseAlVoltant(radi, g);

      // Fem créixer el radi 5cm
      // Posar un radi més gran que el tamany del mapa faria més dificil genera una mostra vàlida
      if (radi < map_.info.height or radi < map_.info.width)
      {
          radi += 0.05;
      }
  }
  return g;
}
void ExploraFronteraMajor::treballa()
{
    if (!exploracio_iniciada_)
        return;

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

void ExploraFronteraMajor::acaba()
{
    double t = (ros::Time::now() - inici_exploracio_).toSec();
    int t_min = int(t)/60;
    int t_sec = int(t)%60;

    printf("//////////////////////////////////////////////\n");
    printf("/////////// EXPLORACIo ACABADA! //////////////\n");
    printf("//////////////////////////////////////////////\n");
    printf("\tEnviats %d goals (arribats %d)\n", num_goals_enviats_, num_goals_ok_);
    printf("\tDistancia recorreguda %.2f m\n", distancia_recorreguda_);
    printf("\tDuracio %2.2i:%2.2i min\n", t_min, t_sec);
    printf("\tExplorat %.2f m^2 (%d celles)\n", celles_explorades_*map_.info.resolution*map_.info.resolution, celles_explorades_);
    printf("!!!!!! Si vols salvar el mapa, recorda fer:\n\trosrun map_server map_saver -f my_map_name\n\n\n");

    ros::shutdown();
}

///// FUNCIONS AUXILIARS //////////////////////////////////////////////////////////////////////
geometry_msgs::Pose ExploraFronteraMajor::generaRandomPoseAlVoltant(float radius, const geometry_msgs::Pose& referencia)
{
  geometry_msgs::Pose goal_pose;

  if (radius <= 0)
  {
      ROS_WARN("getRandomPose: radius must be > 0. Changed to 1");
      radius = 1;
  }

  // dona una pose entre +-radius al voltant de referencia
  //srand((unsigned)time(NULL));
  float rand_yaw = 2*M_PI * (rand()%100)/100.0;
  float rand_r = radius*(rand()%100)/100.0;

  goal_pose.position.x = referencia.position.x + rand_r * cos(rand_yaw);
  goal_pose.position.y = referencia.position.y + rand_r * sin(rand_yaw);
  goal_pose.orientation = tf::createQuaternionMsgFromYaw(tf::getYaw(referencia.orientation) + rand_yaw);

  return goal_pose;
}

bool ExploraFronteraMajor::esGoalValid(const geometry_msgs::Point & point, double & path_length)
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
      ROS_INFO("Goal Valid! Distancia total de la trajectoria al goal: %f m", path_length);
      valid=true;
    }
  }
  else
    ROS_ERROR("Failed to call service get_plan");

  return valid;
}

double ExploraFronteraMajor::calculaLongitudPlan(std::vector<geometry_msgs::PoseStamped> poses)
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

// FUNCIONS DE NAVEGACIo ////////////////////////////////////////////////////////////////////////////////////////
//moveRobot: envia un goal al robot
bool ExploraFronteraMajor::moveRobot(const geometry_msgs::Pose& goal_pose)
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

  printf(">>> Status de l'exploracio:\n\tEnviats %d goals (assolits %d). Distancia recorreguda %.2f m. Han passat %2.2i:%2.2i min. Explorats %.2f m^2 (%d cel.les)\n",
           num_goals_enviats_,
           num_goals_ok_,
           distancia_recorreguda_,
           elapsed_time_minutes, elapsed_time_seconds,
           celles_explorades_*map_.info.resolution*map_.info.resolution,
           celles_explorades_);

  action_move_base_.sendGoal(goal,
                             boost::bind(&ExploraFronteraMajor::move_baseDone, this, _1, _2),
                             actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction>::SimpleActiveCallback(),
                             actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction>::SimpleFeedbackCallback());
  robot_status_=0; //movent-se
  return true;
}

//move_baseDone: es crida quan el robot assoleix un goal o es cancela per alguna rao
void ExploraFronteraMajor::move_baseDone(const actionlib::SimpleClientGoalState& state,  const move_base_msgs::MoveBaseResultConstPtr& result)
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

// Calcula la posicio actual a través de TF
bool ExploraFronteraMajor::actualitzaPosicioRobot()
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
    ExploraFronteraMajor node_explora(nh);
    ros::Rate loop_rate(10);

    while (ros::ok())
    {
        ros::spinOnce();
        loop_rate.sleep();

        node_explora.treballa();
    }
    return 0;
}

