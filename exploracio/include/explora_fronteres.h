#ifndef INCLUDE_EXPLORA_FRONTERES_H_
#define INCLUDE_EXPLORA_FRONTERES_H_

#include <ros/ros.h>
#include <vector>
#include "visualization_msgs/MarkerArray.h"
#include "nav_msgs/OccupancyGrid.h"
#include "exploracio/Fronteres.h"

#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>

#include <tf/transform_datatypes.h>
#include <tf/transform_listener.h>

#include "nav_msgs/GetPlan.h"

class ExploraFronteraMajor
{
    private:
      ros::NodeHandle nh_;
      ros::Publisher goal_marker_pub_;
      ros::Subscriber fronteres_sub_, map_sub_;
      ros::ServiceClient get_plan_client_;

      actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> action_move_base_;
      tf::TransformListener listener_;

      int robot_status_; //0: movent-se, 1: goal assolit, 2: no s'ha pogut arribar al goal
      geometry_msgs::Pose target_goal_; //últim goal enviat
      geometry_msgs::Pose robot_pose_; // posició actual del robot
      geometry_msgs::Pose prev_robot_pose_; //última posició del robot (s'utilitza per calcular distància recorreguda)

      nav_msgs::OccupancyGrid map_;
      exploracio::Fronteres fronteres_msg_;

      // estadístiques
      int num_celles_; //nombre de cel·les del mapa (height*width)
      int num_goals_enviats_; //total goals enviats
      int num_goals_ok_; // total gols assolits
      double distancia_recorreguda_; // distància recorreguda al llarg de l'exploració (m)
      ros::Time inici_exploracio_; // per calcular el temps total de l'exploració
      int celles_explorades_; // nombre de cel·les explorades
      bool exploracio_acabada_; // flag per finalitar l'exploració
      bool exploracio_iniciada_; // flag per iniciar l'exploració

    public:
      ExploraFronteraMajor(ros::NodeHandle& nh);
      void treballa();

    private:
      void mapCallback(const nav_msgs::OccupancyGrid::ConstPtr& msg);
      void fronteresCallback(const exploracio::Fronteres::ConstPtr& msg);

      // METODE
      bool replanifica();
      geometry_msgs::Pose decideixGoal();
      void acaba();

      // AUXILIARS
      geometry_msgs::Pose generaRandomPoseAlVoltant(float radius, const geometry_msgs::Pose& referencia);
      bool esGoalValid(const geometry_msgs::Point & point, double & path_length);
      double calculaLongitudPlan(std::vector<geometry_msgs::PoseStamped> poses);

      // LOCALITZACIÓ i NAVEGACIÓ
      bool moveRobot(const geometry_msgs::Pose& goal_pose);
      void move_baseDone(const actionlib::SimpleClientGoalState& state,  const move_base_msgs::MoveBaseResultConstPtr& result);
      void move_baseActive();
      bool actualitzaPosicioRobot();
};

#endif /* INCLUDE_EXPLORA_FRONTERES_H_ */
