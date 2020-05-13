#include "troba_fronteres.h"

TrobaFronteres::TrobaFronteres(ros::NodeHandle& nh)
{
    nh_ = nh;

    nh_.param<int>("tamany_min_frontera", min_frontier_size_, 5);

    fronteres_pub_       = nh_.advertise<exploracio::Fronteres>("fronteres", 1);
    mapa_fronteres_pub_  = nh_.advertise<nav_msgs::OccupancyGrid>("mapa_fronteres", 1);
    mapa_lliures_pub_    = nh_.advertise<nav_msgs::OccupancyGrid>("mapa_lliures", 1);
    mapa_filtrat_pub_    = nh_.advertise<nav_msgs::OccupancyGrid>("mapa_filtrat", 1);
    markers_pub_         = nh_.advertise<visualization_msgs::MarkerArray>("markers", 1);
    map_sub_             = nh_.subscribe("/map", 1, &TrobaFronteres::mapCallback,this);
}

void TrobaFronteres::mapCallback(const nav_msgs::OccupancyGrid::ConstPtr& msg)
{
    ROS_INFO("mapa rebut!");

    nav_msgs::OccupancyGrid mapa_occupacio = *msg;
    nav_msgs::OccupancyGrid mapa_fronteres = *msg;
    nav_msgs::OccupancyGrid mapa_lliures = *msg;

    // reseteja mapes
    mapa_fronteres.data.assign(mapa_fronteres.data.size(), 0);
    mapa_lliures.data.assign(mapa_lliures.data.size(), 0);

    // FILTRAR CEL·LES LLIURES DESCONNECTADES
    // crea mapa lliures (assigna si és lliure cada cel·la)
    for(int i = 0; i < mapa_lliures.data.size(); ++i)
    {
        if(mapa_occupacio.data[i] == 0)
            mapa_lliures.data[i] = 100;
        //else
        //    mapa_lliures.data[i] = 0;
    }
    // Etiqueta lliures (connected cells)
    std::map<int,int> labels_lliures_sizes;
    std::vector<int> labels_lliures = twoPassLabeling(mapa_lliures, labels_lliures_sizes);
    // Classifiquem com a desconegudes tot els grups lliures menys el més gran
    int remaining_label = std::max_element(labels_lliures_sizes.begin(),
                                           labels_lliures_sizes.end(),
                                           [] (const std::pair<int,int> & p1, const std::pair<int,int> & p2) {return p1.second < p2.second;})->first;
    for(int i = 0; i < mapa_occupacio.data.size(); ++i)
    {
        if (mapa_occupacio.data[i] == 0 and labels_lliures[i] != remaining_label)
        {
            mapa_occupacio.data[i] = -1;
            mapa_lliures.data[i] = 0;
        }
    }
    // publicar mapa_lliures
    mapa_lliures_pub_.publish(mapa_lliures);
    ROS_INFO("mapa de lliures publicat!");

    // publicar mapa_lliures
    mapa_filtrat_pub_.publish(mapa_occupacio);
    ROS_INFO("mapa filtrat publicat!");

    // TROBAR FRONTERES
    // crea mapa fronteres (assigna si és frontera cada cel·la)
    for(int i = 0; i < mapa_fronteres.data.size(); ++i)
    {
        if(esFrontera(i, mapa_occupacio))
            mapa_fronteres.data[i] = 100;
        //else
        //    mapa_fronteres.data[i] = 0;
    }

    // publicar mapa_fronteres
    mapa_fronteres_pub_.publish(mapa_fronteres);
    ROS_INFO("mapa de fronteres publicat!");

    // Etiqueta fronteres (connected cells)
    std::map<int,int> labels_sizes;
    std::vector<int> labels = twoPassLabeling(mapa_fronteres, labels_sizes);

    // Crea i omple missatge fronteres
    exploracio::Fronteres fronteres_msg;
    fronteres_msg.header = msg->header;
    fronteres_msg.fronteres.clear();
    for (int i = 0; i < labels.size(); ++i)
    {
        if(labels[i]!=0) //cel·la etiquetada
        {
            // Si tamany frontera massa petit, continuem
            if (labels_sizes[labels[i]] < min_frontier_size_)
                continue;

            // Busca frontera ja existent
            bool new_label = true;
            for (unsigned int j = 0; j < fronteres_msg.fronteres.size(); j++)
            {
                // trobada
                if (fronteres_msg.fronteres[j].id == labels[i])
                {
                    fronteres_msg.fronteres[j].celles_celles.push_back(i);
                    fronteres_msg.fronteres[j].celles_punts.push_back(cell2point(i,mapa_fronteres));
                    new_label = false;
                    break;
                }
            }
            // no trobada: creem nova frontera
            if (new_label)
            {
                exploracio::Frontera nova_frontera;
                nova_frontera.id = labels[i];
                nova_frontera.size = labels_sizes[labels[i]];
                nova_frontera.celles_celles.push_back(i);
                nova_frontera.celles_punts.push_back(cell2point(i,mapa_fronteres));
                fronteres_msg.fronteres.push_back(nova_frontera);
            }
        }
    }

    // Calcula cella central
    for(unsigned int i = 0; i < fronteres_msg.fronteres.size(); ++i)
    {
        int label = fronteres_msg.fronteres[i].id;

        // order the frontier cells
        std::deque<int> ordered_cells(0);
        ordered_cells.push_back(fronteres_msg.fronteres[i].celles_celles.front());
        while (ordered_cells.size() < fronteres_msg.fronteres[i].size)
        {
            int initial_size = ordered_cells.size();

            // connect cells to first cell
            std::vector<int> frontAdjacentPoints = getAdjacentPoints(ordered_cells.front(), mapa_fronteres);
            for (unsigned int k = 0; k<frontAdjacentPoints.size(); k++)
                if (frontAdjacentPoints[k] != -1 && labels[frontAdjacentPoints[k]] == label && std::find(ordered_cells.begin(), ordered_cells.end(), frontAdjacentPoints[k]) == ordered_cells.end() )
                {
                    ordered_cells.push_front(frontAdjacentPoints[k]);
                    break;
                }

            // connect cells to last cell
            std::vector<int> backAdjacentPoints = getAdjacentPoints(ordered_cells.back(), mapa_fronteres);
            for (unsigned int k = 0; k<backAdjacentPoints.size(); k++)
                if (backAdjacentPoints[k] != -1 && labels[backAdjacentPoints[k]] == label && std::find(ordered_cells.begin(), ordered_cells.end(), backAdjacentPoints[k]) == ordered_cells.end() )
                {
                    ordered_cells.push_back(backAdjacentPoints[k]);
                    break;
                }

            if (initial_size == ordered_cells.size() && ordered_cells.size() < fronteres_msg.fronteres[i].size)
                break;
        }
        // center cell
        fronteres_msg.fronteres[i].centre_cella    = ordered_cells[ordered_cells.size() / 2];
        fronteres_msg.fronteres[i].centre_punt     = cell2point(fronteres_msg.fronteres[i].centre_cella, mapa_fronteres);

        // find the close free cell of the middle frontier cell
        std::vector<int> adjacentPoints = getAdjacentPoints(fronteres_msg.fronteres[i].centre_cella, mapa_fronteres);
        for (unsigned int k = 0; k<adjacentPoints.size(); k++)
        {
            if (mapa_occupacio.data[adjacentPoints[k]] == 0) // free neighbor cell
            {
                fronteres_msg.fronteres[i].centre_lliure_cella = adjacentPoints[k];
                break;
            }
            if (k == 7)
                ROS_ERROR("findFrontiers: No free cell close to the center frontier cell!");
        }
        fronteres_msg.fronteres[i].centre_lliure_punt = cell2point(fronteres_msg.fronteres[i].centre_lliure_cella, mapa_fronteres);
    }

    // Publica
    fronteres_pub_.publish(fronteres_msg);
    ROS_INFO("fronteres publicat!");
    publishMarkers(fronteres_msg);
    ROS_INFO("marker array publicat!");
}

// Check if a cell is frontier
bool TrobaFronteres::esFrontera(const int& cell, const nav_msgs::OccupancyGrid& mapa) const
{
    if(mapa.data[cell] == -1) //check if it is unknown
    {
        auto straightPoints = getStraightPoints(cell,mapa);
        for(int i = 0; i < straightPoints.size(); ++i)
            if(straightPoints[i] != -1 && mapa.data[straightPoints[i]] == 0) //check if any neigbor is free space
                return true;
    }
    // If it is obstacle or free can not be frontier
    return false;
}

// Two pass labeling to label frontiers [http://en.wikipedia.org/wiki/Connected-component_labeling]
std::vector<int> TrobaFronteres::twoPassLabeling(const nav_msgs::OccupancyGrid& mapa_etiquetar, std::map<int,int>& labels_sizes) const
{
    labels_sizes.clear();
    std::vector<int> labels(mapa_etiquetar.data.size());
    labels.assign(mapa_etiquetar.data.begin(), mapa_etiquetar.data.end());

    std::vector<int> neigh_labels;
    std::vector<int> rank(1000);
    std::vector<int> parent(1000);
    boost::disjoint_sets<int*,int*> dj_set(&rank[0], &parent[0]);
    int current_label_=1;

    // 1ST PASS: Assign temporary labels to frontiers and establish relationships
    for(unsigned int i = 0; i < mapa_etiquetar.data.size(); i++)
    {
        if( mapa_etiquetar.data[i] != 0)
        {
            neigh_labels.clear();
            // Find 8-connectivity neighbours already labeled
            if(upleftCell(i,mapa_etiquetar)  != -1 && labels[upleftCell(i,mapa_etiquetar)]  != 0) neigh_labels.push_back(labels[upleftCell(i,mapa_etiquetar)]);
            if(upCell(i,mapa_etiquetar)      != -1 && labels[upCell(i,mapa_etiquetar)]      != 0) neigh_labels.push_back(labels[upCell(i,mapa_etiquetar)]);
            if(uprightCell(i,mapa_etiquetar) != -1 && labels[uprightCell(i,mapa_etiquetar)] != 0) neigh_labels.push_back(labels[uprightCell(i,mapa_etiquetar)]);
            if(leftCell(i,mapa_etiquetar)    != -1 && labels[leftCell(i,mapa_etiquetar)]    != 0) neigh_labels.push_back(labels[leftCell(i,mapa_etiquetar)]);

            if(neigh_labels.empty())                                                  // case: No neighbours
            {
                dj_set.make_set(current_label_);                                        //   create new set of labels
                labels[i] = current_label_;                                            //   update cell's label
                current_label_++;                                                       //   update label
            }
            else                                                                      // case: With neighbours
            {
                labels[i] = *std::min_element(neigh_labels.begin(), neigh_labels.end());//   choose minimum label of the neighbours
                for(unsigned int j = 0; j < neigh_labels.size(); ++j)                   //   update neighbours sets
                    dj_set.union_set(labels[i],neigh_labels[j]);                          //   unite sets minimum label with the others
            }
        }
    }

    // 2ND PASS: Assign final label
    dj_set.compress_sets(labels.begin(), labels.end());
    // compress sets for efficiency
    for(unsigned int i = 0; i < mapa_etiquetar.data.size(); i++)
        if( labels[i] != 0)
        {
            // relabel each element with the lowest equivalent label
            labels[i] = dj_set.find_set(labels[i]);
            // increment the size of the label
            if (labels_sizes.count(labels[i]) == 0)
                labels_sizes[labels[i]] = 1;
            else
                labels_sizes[labels[i]]++;
        }

    return labels;
}

void TrobaFronteres::publishMarkers(const exploracio::Fronteres& fronteres_msg)
{

    // redimensionar
    markers_.markers.resize(fronteres_msg.fronteres.size()*3+1); // cada frontera: celles_punts, centre_lliure_punt i id

    // deleteall
    markers_.markers[0].action = visualization_msgs::Marker::DELETEALL;

    // omplir
    for (int i = 0; i < fronteres_msg.fronteres.size(); i++)
    {
        std_msgs::ColorRGBA c;
        c.a = 1.0;
        c.r = sin(fronteres_msg.fronteres[i].id*0.3);
        c.g = sin(fronteres_msg.fronteres[i].id*0.3 + 2*M_PI/3);
        c.b = sin(fronteres_msg.fronteres[i].id*0.3 + 4*M_PI/3);

        // punts
        visualization_msgs::Marker marker_punts;
        marker_punts.header.frame_id = fronteres_msg.header.frame_id;
        marker_punts.header.stamp = ros::Time::now();
        marker_punts.lifetime = ros::Duration(0);
        marker_punts.type = visualization_msgs::Marker::POINTS;
        marker_punts.pose.orientation.x = marker_punts.pose.orientation.y = marker_punts.pose.orientation.z = 0; marker_punts.pose.orientation.w = 1;
        marker_punts.points = fronteres_msg.fronteres[i].celles_punts;
        marker_punts.scale.x = marker_punts.scale.y = marker_punts.scale.z = 0.1;
        marker_punts.colors = std::vector<std_msgs::ColorRGBA>(marker_punts.points.size(),c);
        marker_punts.ns = "celles";
        marker_punts.id = 3*i;
        markers_.markers[3*i+1] = marker_punts;

        // centre lliure punt
        visualization_msgs::Marker marker_centre;
        marker_centre.header.frame_id = fronteres_msg.header.frame_id;
        marker_centre.header.stamp = ros::Time::now();
        marker_centre.lifetime = ros::Duration(0);
        marker_centre.type = visualization_msgs::Marker::CYLINDER;
        marker_centre.scale.x = marker_centre.scale.y = 0.1;
        marker_centre.scale.z = 0.5;
        marker_centre.color = c;
        marker_centre.ns = "centres";
        marker_centre.id = 3*i+1;
        marker_centre.pose.position.x = fronteres_msg.fronteres[i].centre_lliure_punt.x;
        marker_centre.pose.position.y = fronteres_msg.fronteres[i].centre_lliure_punt.y;
        marker_centre.pose.position.z = marker_centre.scale.z/2;
        marker_centre.pose.orientation.x = marker_centre.pose.orientation.y = marker_centre.pose.orientation.z = 0; marker_centre.pose.orientation.w = 1;
        markers_.markers[3*i+2] = marker_centre;

        // id text
        visualization_msgs::Marker marker_id;
        marker_id.header.frame_id = fronteres_msg.header.frame_id;
        marker_id.header.stamp = ros::Time::now();
        marker_id.lifetime = ros::Duration(0);
        marker_id.type = visualization_msgs::Marker::TEXT_VIEW_FACING;
        marker_id.scale.x = marker_id.scale.y = 1;
        marker_id.scale.z = 0.5;
        marker_id.text = std::to_string(fronteres_msg.fronteres[i].id);
        marker_id.color = c;
        marker_id.pose = marker_centre.pose;
        marker_id.pose.position.z = marker_centre.scale.z + 0.2;
        marker_id.ns = "ids";
        marker_id.id = 3*i+2;
        markers_.markers[3*i+3] = marker_id;
    }
    // publicar
    markers_pub_.publish(markers_);
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "troba_fronteres_node");
    ros::NodeHandle nh("~");
    TrobaFronteres node_fronteres(nh);
    ros::Rate loop_rate(10);

    while (ros::ok())
    {
        ros::spinOnce();
        loop_rate.sleep();
    }
    return 0;
}

