#ifndef INCLUDE_TROBA_FRONTERES_H_
#define INCLUDE_TROBA_FRONTERES_H_

#include <termios.h>
#include <stdio.h>
#include <ros/ros.h>
#include <vector>
#include <deque>
#include <algorithm>
#include "visualization_msgs/MarkerArray.h"
#include "nav_msgs/OccupancyGrid.h"
#include "std_msgs/ColorRGBA.h"
#include "exploracio/Fronteres.h"
#include <boost/pending/disjoint_sets.hpp>
#include <numeric>
#include <algorithm>

class TrobaFronteres
{
    private:
      ros::NodeHandle nh_;
      ros::Publisher fronteres_pub_, mapa_fronteres_pub_, mapa_lliures_pub_, mapa_filtrat_pub_, markers_pub_;
      ros::Subscriber map_sub_;
      visualization_msgs::MarkerArray markers_;
      int min_frontier_size_; // tamany minim de frontera

    public:
      TrobaFronteres(ros::NodeHandle& nh);

    private:
      void mapCallback(const nav_msgs::OccupancyGrid::ConstPtr& msg);
      std::vector<int> twoPassLabeling(const nav_msgs::OccupancyGrid& mapa_fronteres, std::map<int,int>& labels_sizes) const;
      bool esFrontera(const int& cell, const nav_msgs::OccupancyGrid& mapa) const;
      void publishMarkers(const exploracio::Fronteres& fronteres_msg);

      // UTILS
      int point2cell(const geometry_msgs::Point & point, const nav_msgs::OccupancyGrid& map_) const
      {
          if(point.x <= map_.info.origin.position.x || point.x >= map_.info.width*map_.info.resolution + map_.info.origin.position.x  ||
                  point.y <= map_.info.origin.position.y || point.y >= map_.info.height*map_.info.resolution+ map_.info.origin.position.y)
          {
              return -1;
          }

          int x_cell = floor0((point.x - map_.info.origin.position.x)/map_.info.resolution);
          int y_cell = floor0((point.y - map_.info.origin.position.y)/map_.info.resolution);
          int cell = x_cell + (y_cell)*map_.info.width;
          return cell;
      }
      geometry_msgs::Point cell2point(const int & cell, const nav_msgs::OccupancyGrid& map_) const
      {
          geometry_msgs::Point point;
          point.x = (cell % map_.info.width)*map_.info.resolution + map_.info.origin.position.x + map_.info.resolution / 2;
          point.y = floor(cell/map_.info.width)*map_.info.resolution + map_.info.origin.position.y + map_.info.resolution / 2;
          return point;
      }

      std::vector<int> getStraightPoints(const int& cell, const nav_msgs::OccupancyGrid& map_) const
      {
          return std::vector<int>({leftCell(cell, map_),
                                   upCell(cell, map_),
                                   rightCell(cell, map_),
                                   downCell(cell, map_)});
      }
      std::vector<int> getAdjacentPoints(const int& cell, const nav_msgs::OccupancyGrid& map_) const
      {
          return std::vector<int>({leftCell(cell, map_),
                                  upCell(cell, map_),
                                  rightCell(cell, map_),
                                  downCell(cell, map_),
                                  upleftCell(cell, map_),
                                  uprightCell(cell, map_),
                                  downrightCell(cell, map_),
                                  downleftCell(cell, map_)});
      }
      int rightCell(const int& cell, const nav_msgs::OccupancyGrid& map_) const
      {
          // only go left if no index error and if current cell is not already on the left boundary
          if((cell % map_.info.width != 0))
              return cell+1;

          return -1;
      }
      int uprightCell(const int& cell, const nav_msgs::OccupancyGrid& map_) const
      {
          if((cell % map_.info.width != 0) && (cell >= (int)map_.info.width))
              return cell-map_.info.width+1;

          return -1;
      }
      int upCell(const int& cell, const nav_msgs::OccupancyGrid& map_) const
      {
          if(cell >= (int)map_.info.width)
              return cell-map_.info.width;

          return -1;
      }
      int upleftCell(const int& cell, const nav_msgs::OccupancyGrid& map_) const
      {
          if((cell >= (int)map_.info.width) && ((cell + 1) % (int)map_.info.width != 0))
              return cell-map_.info.width-1;

          return -1;
      }
      int leftCell(const int& cell, const nav_msgs::OccupancyGrid& map_) const
      {
          if((cell + 1) % map_.info.width != 0)
              return cell-1;

          return -1;
      }
      int downleftCell(const int& cell, const nav_msgs::OccupancyGrid& map_) const
      {
          if(((cell + 1) % map_.info.width != 0) && ((cell/map_.info.width) < (map_.info.height-1)))
              return cell+map_.info.width-1;

          return -1;
      }
      int downCell(const int& cell, const nav_msgs::OccupancyGrid& map_) const
      {
          if((cell/map_.info.width) < (map_.info.height-1))
              return cell+map_.info.width;

          return -1;
      }
      int downrightCell(const int& cell, const nav_msgs::OccupancyGrid& map_) const
      {
          if(((cell/map_.info.width) < (map_.info.height-1)) && (cell % map_.info.width != 0))
              return cell+map_.info.width+1;

          return -1;
      }
      int floor0(const float& value) const
      {
          if (value < 0.0)
              return ceil( value );
          else
              return floor( value );
      }
};

#endif /* INCLUDE_TROBA_FRONTERES_H_ */
