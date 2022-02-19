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
#include <set>

class edge{
    private:
        std::string vertex1;
        std::string vertex2;
        float cost;
    public:
        edge(std::string __vertex1, std::string __vertex2, float __cost):
            vertex1{__vertex1}, vertex2{__vertex2}, cost{__cost}{}
        std::string get_c1() const{  return vertex1;}
        std::string get_c2() const{  return vertex2;}
        float get_cost() const{  return cost;}
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
        std::map<edge_pair, float> cost;

        int expanded;
        int generated;
        float total_cost;
        
        graph(std::string infile): expanded{0}, generated{0}, total_cost{0}{
            for(const auto& e : load_edges(std::ifstream{infile}))
                add_edge(e);
        }

        edge_pair make_edge_pair(std::string vertex1, std::string vertex2){
            return edge_pair{vertex1, vertex2};
        }

        void add_edge(edge e){
            adj_list[e.get_c1()].push_back(e.get_c2());
            adj_list[e.get_c2()].push_back(e.get_c1());
            cost[make_edge_pair(e.get_c1(), e.get_c2())] = e.get_cost();
            cost[make_edge_pair(e.get_c2(), e.get_c1())] = e.get_cost();
        }

        void print_node(std::string vertex1, std::string vertex2){
            auto is_node = find_node(vertex1, vertex2);
            std::cout.precision(1);
            
            std::cout << "nodes expanded: " << expanded << std::endl;
            std::cout << "nodes generated: " << generated << std::endl;
            if(is_node)
                std::cout << "distance: " << std::fixed << total_cost << "km\n";
            else
                std::cout << "distance: infinity\n";

            std::cout << "node: \n";
            if(!is_node){
                std::cout << "none\n";
                return;
            }
        }
        
        bool find_node(std::string vertex1, std::string vertex2){
            typedef std::pair<std::string, float> node;
            auto cmp = [](node lhs, node rhs){
                return lhs.second > rhs.second;
            };
            std::priority_queue<node,
                std::vector<node>, decltype(cmp)> q(cmp);
            q.push(node{vertex1, total_cost});
            std::set<std::string> closed;
            auto min = total_cost;

            while(!q.empty()){
                node vertex = q.top();
                q.pop();
                expanded++;
                if(closed.find(vertex.first) != closed.end())
                    continue;
                if(vertex.second < total_cost && !vertex.first.compare(vertex2))
                    total_cost = vertex.second;
                else if(total_cost)
                    continue;
                for(auto adj_vertex : adj_list[vertex.first]){
                    auto adj_cost{
                        vertex.second + cost[make_edge_pair(vertex.first, adj_vertex)]
                    };
                    q.push(node{adj_vertex, adj_cost});
                    auto found = !adj_vertex.compare(vertex2);
                    if(found && !total_cost)
                        total_cost = adj_cost;
                    else if(found && adj_cost < total_cost)
                        total_cost = adj_cost;
                }
                closed.insert(vertex.first);
            }
            return total_cost;
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
    g.print_node(origin_city, destination_city);
    return 0;
}