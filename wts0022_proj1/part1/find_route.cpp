//  William Sigala
//  CSE 4308/5360
//  Asssignment 1

#include <utility>
#include <vector>
#include <fstream>
#include <iostream>
#include <string>
#include <map>
#include <list>
#include <stack>
#include <queue>

class edge{
    private:
        std::string city1;
        std::string city2;
        float weight;
    public:
        edge(std::string __city1, std::string __city2, float __weight):
            city1{__city1}, city2{__city2}, weight{__weight}{}
        std::string get_c1() const{  return city1;}
        std::string get_c2() const{  return city2;}
        float get_weight() const{  return weight;}
};

std::vector<edge> load_edges(std::ifstream ifs){
    std::string arg1, arg2, arg3;
    std::vector<edge> edge_set;

    while(std::getline(ifs, arg1, ' ')){
        std::getline(ifs, arg2, ' ');
        std::getline(ifs, arg3);

        if(!arg1.compare("END") && !arg2.compare("OF"))
            break;
        edge_set.push_back(edge{arg1, arg2, std::stof(arg3)});
    }
    ifs.close();
    return edge_set;
}

typedef std::pair<std::string, std::string> edge_pair;

class graph {
    public:
        std::map<std::string, std::list<std::string>> adj_list;
        std::map<std::string, bool> visited;
        std::map<std::string, std::string> path;
        std::map<edge_pair, float> cost;

        int expanded;
        int generated;
        float total_distance;
        
        graph(std::string infile): expanded{0}, generated{0}, total_distance{0}{
            for(const auto& e : load_edges(std::ifstream{infile}))
                add_edge(e);
        }

        edge_pair* make_edge_pair(std::string city1, std::string city2){
            return new edge_pair{city1, city2};
        }

        void add_edge(edge e){
            path[e.get_c1()] = "";
            path[e.get_c2()] = "";
            visited[e.get_c1()] = false;
            visited[e.get_c2()] = false;
            adj_list[e.get_c1()].push_back(e.get_c2());
            adj_list[e.get_c2()].push_back(e.get_c1());
            cost[*make_edge_pair(e.get_c1(), e.get_c2())] = e.get_weight();
            cost[*make_edge_pair(e.get_c2(), e.get_c1())] = e.get_weight();
        }

        void print_route(std::string city1, std::string city2){
            auto is_route = find_route(city1, city2);
            std::stack<std::string> stack;
            std::vector<edge> route_edges;
            std::string prev_city = city1;
            std::cout.precision(1);

            //  Every node that is visited is generated
            
            for(const auto& item : visited){
                if(item.second)
                    generated++;
            }

            while(path[city2].compare("")) {
                stack.push(city2);
                city2 = path[city2];
            }
            
            while(!stack.empty()) {
                auto edge_distance = cost[*make_edge_pair(prev_city, stack.top())];
                total_distance += edge_distance;
                route_edges.push_back(edge{prev_city, stack.top(), edge_distance});
                prev_city = stack.top();
                stack.pop();
            }

            std::cout << "nodes expanded: " << expanded << std::endl;
            std::cout << "nodes generated: " << generated << std::endl;
            if(is_route)
                std::cout << "distance: " << std::fixed << total_distance << "km\n";
            else
                std::cout << "distance: infinity\n";

            std::cout << "route: \n";
            if(!is_route){
                std::cout << "none\n";
                return;
            }
            
            for(const auto& e : route_edges){
                std::cout << e.get_c1() << " to " << e.get_c2() << " ";
                std::cout << std::fixed << e.get_weight();
                std::cout << " km" << std::endl;
            }
            
        }
        
        bool find_route(std::string city1, std::string city2){
            typedef std::pair<std::string, float> route;
            auto cmp = [](route lhs, route rhs){
                return lhs.second > rhs.second;
            };
            std::priority_queue<route, std::vector<route>, decltype(cmp)> q(cmp);
            q.push(route{city1, 0});
            visited[city1] = true;

            while(!q.empty()){
                route city = q.top();
                q.pop();
                expanded += 1;  //  city node gets expanded
                for(auto adj_city: adj_list[city.first]){
                    if(!visited[adj_city]){
                        visited[adj_city] = true;
                        auto adj_cost = cost[*make_edge_pair(city.first, adj_city)];
                        q.push(route{adj_city, adj_cost});
                        path[adj_city] = city.first;
                        if(!adj_city.compare(city2))
                            return true;
                    }
                }
            }
            
            return false;
        }
};

int main(int argc, char* argv[]){
    if(argc != 4 && argc != 5){
        std::cout << "Invalid argument amount. " << argc - 1 << "given\n";
        return 1;
    }

    std::string origin_city = argv[2];
    std::string destination_city = argv[3];
    std::string heuristic_filename = (argc == 5) ? argv[4] : std::string{};
    graph g{argv[1]};
    g.print_route(origin_city, destination_city);
    return 0;
}