//  William Sigala
//  CSE 4308/5360
//  Asssignment 1

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
        double weight;
    public:
        edge(std::string __city1, std::string __city2, double __weight):
            city1{__city1}, city2{__city2}, weight{__weight}{}
        std::string get_c1() const{  return city1;}
        std::string get_c2() const{  return city2;}
        double get_weight() const{  return weight;}
};

void load_edges(std::ifstream ifs, std::vector<edge>& edge_set){
    std::string arg1, arg2, arg3;

    while(std::getline(ifs, arg1, ' ')){
        std::getline(ifs, arg2, ' ');
        std::getline(ifs, arg3);

        if(!arg1.compare("END") && !arg2.compare("OF"))
            break;
        edge_set.push_back(edge{arg1, arg2, std::stod(arg3)});
    }
    ifs.close();
}

class graph {
    public:
        std::map<std::string, bool> visited;
        std::map<std::string, std::list<std::string>> adj_list;
        std::map<std::string, std::string> route;
        std::vector<edge> edge_set;

        int expanded;
        int generated;
        double total_distance;
        
        graph(std::string infile): expanded{0}, generated{0}{
            load_edges(std::ifstream{infile}, edge_set);
            for(const auto e : edge_set)
                add_edge(e);
        }

        edge* get_edge(std::string city1, std::string city2){
            for(edge& e : edge_set){
                if(!e.get_c1().compare(city1) && !e.get_c2().compare(city2))
                    return &e;
                if(!e.get_c2().compare(city1) && !e.get_c1().compare(city2))
                    return &e;
            }
            return nullptr;
        }

        void add_edge(edge e){
            adj_list[e.get_c1()].push_back(e.get_c2());
            visited[e.get_c1()] = false;
            route[e.get_c1()] = "";
        }

        void print_route(std::string city1, std::string city2){
            auto is_route = find_route(city1, city2);
            std::stack<std::string> stack;
            std::vector<edge> route_edges;
            std::string prev_city = city1;
            std::cout.precision(1);

            while(route[city2].compare("")) {
                stack.push(city2);
                city2 = route[city2];
            }
            
            while(!stack.empty()) {
                auto edge_distance = get_edge(prev_city, stack.top()) -> get_weight();
                total_distance += edge_distance;
                route_edges.push_back(edge{prev_city, stack.top(), edge_distance});
                prev_city = stack.top();
                stack.pop();
            }

            std::cout << "nodes expanded: " << visited.size() << std::endl;
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
            std::queue<std::string> q;

            q.push(city1);
            visited[city1] = true;

            while(!q.empty()){
                std::string city = q.front();
                q.pop();
                for(std::string adj_city: adj_list[city]){
                    if(!visited[adj_city]){
                        q.push(adj_city);
                        visited[adj_city] = true;
                        route[adj_city] = city;
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
        std::cout << "Invalid arguments. " << argc << "given\n";
        return 1;
    }

    std::string origin_city = argv[2];
    std::string destination_city = argv[3];
    std::string heuristic_filename = (argc == 5) ? argv[4] : std::string{};

    graph g{argv[1]};
    g.print_route(origin_city, destination_city);
    return 0;
}