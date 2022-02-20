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


typedef std::pair<std::string, std::string> edge_pair;
typedef std::pair<std::string, float> node;

class edge{
    private:
        std::string vertex1, vertex2;
        float cost;
    public:
        edge(std::string __vertex1, std::string __vertex2, float __cost):
            vertex1{__vertex1}, vertex2{__vertex2}, cost{__cost}{}
        std::string get_c1() const{  return vertex1;}
        std::string get_c2() const{  return vertex2;}
        float get_cost() const{  return cost;}
};

std::vector<edge> load_edges(std::ifstream ifs){
    std::string args, end = "END OF INPUT";
    std::vector<edge> edge_set;

    while(std::getline(ifs, args)){
        if(args.find(end) != std::string::npos)
            break;
        std::string arg1, arg2, arg3;
        auto pos = args.find(' ');
        
        arg1 = args.substr(0, pos);
        args.erase(0, pos + 1);
        arg2 = args.substr(0, pos = args.find(' '));
        args.erase(0, pos + 1);
        arg3 = args.substr(0);
        edge_set.push_back(edge{arg1, arg2, std::stof(arg3)});
    }
    ifs.close();
    return edge_set;
}
std::vector<node> load_heuristics(std::ifstream ifs){
    std::string args, end = "END OF INPUT";
    std::vector<node> h_set;

    while(std::getline(ifs, args)){
        if(args.find(end) != std::string::npos)
            break;
        std::string arg1, arg2;
        auto pos = args.find(' ');
        arg1 = args.substr(0, pos);
        args.erase(0, pos + 1);
        arg2 = args.substr(0);
        h_set.push_back(node{arg1, std::stof(arg2)});
    }
    ifs.close();
    return h_set;
}

class graph {
    private:
        int expanded, generated;
        float total_cost;

        std::map<std::string, std::list<std::string>> adj_list;
        std::map<edge_pair, float> cost;
        std::map<node, node> predecessors;
        std::vector<node> heuristic_vals;
    public:
        graph(std::string infile1, std::string infile2):
            expanded{0}, generated{0}, total_cost{0}{
            for(const auto& e : load_edges(std::ifstream{infile1}))
                add_edge(e);
            if(infile2.compare(""))
                heuristic_vals = load_heuristics(std::ifstream{infile2});
        }

        void add_edge(edge e){
            predecessors[node{e.get_c1(), 0}] = node{e.get_c2(), 0};
            predecessors[node{e.get_c2(), 0}] = node{e.get_c1(), 0};
            adj_list[e.get_c1()].push_back(e.get_c2());
            adj_list[e.get_c2()].push_back(e.get_c1());
            cost[edge_pair{e.get_c1(), e.get_c2()}] = e.get_cost();
            cost[edge_pair{e.get_c2(), e.get_c1()}] = e.get_cost();
        }

        void print_route(std::string vertex1, std::string vertex2){
            auto is_node = find_route(vertex1, vertex2);
            std::cout.precision(1);
            
            std::cout << "nodes expanded: " << expanded << std::endl;
            std::cout << "nodes generated: " << generated << std::endl;
            if(is_node)
                std::cout << "distance: " << std::fixed << total_cost << " km\n";
            else
                std::cout << "distance: infinity\n";

            std::cout << "route: \n";
            if(!is_node){
                std::cout << "none\n";
                return;
            }
            else{
                auto curr = node{vertex2, total_cost};
                std::stack<node> route;
                route.push(curr);

                while(curr.second != 0){
                    curr = predecessors[curr];
                    route.push(curr);
                }

                while(route.size() > 1){
                    std::string first, second; 
                    std::cout << (first = route.top().first) << " to ";
                    route.pop();
                    std::cout << (second = route.top().first) << ", " ;
                    std::cout << std::fixed << cost[edge_pair{first, second}] << " km\n";
                }
            }
        }
        
        bool find_route(std::string vertex1, std::string vertex2){
            if(!vertex1.compare(vertex2))
                return true;
            
            auto cmp = [](node lhs, node rhs){
                return lhs.second > rhs.second;
            };
            std::priority_queue<node,
                std::vector<node>, decltype(cmp)> q(cmp);
            q.push(node{vertex1, total_cost});
            std::set<std::string> closed;
            auto min = total_cost;
            generated++;

            while(!q.empty()){
                node vertex = q.top();
                auto found = !vertex.first.compare(vertex2);
                q.pop();
                // evaluate total cost when found
                if(found && !total_cost)
                    total_cost = vertex.second;
                else if(found && vertex.second < total_cost)
                    total_cost = vertex.second;
                else if(total_cost && vertex.second >= total_cost)
                    continue;
                expanded++;
                //  don't expand if found or in closed
                if(found)
                    continue;
                if(closed.find(vertex.first) != closed.end())
                    continue;

                for(auto adj_vertex : adj_list[vertex.first]){
                    auto adj_cost{
                        vertex.second + cost[edge_pair{vertex.first, adj_vertex}]
                    };
                    auto new_node = node{adj_vertex, adj_cost};

                    if(!predecessors[new_node].second)
                        predecessors[new_node] = vertex;
                    else if(predecessors[new_node].second >= vertex.second)
                        predecessors[new_node] = vertex;
                    q.push(new_node);
                    generated++;
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

    std::string filename = argv[1];
    std::string origin_city = argv[2];
    std::string destination_city = argv[3];
    std::string heuristic_filename = (argc == 5) ? argv[4] : "";
    auto g = new graph{filename, heuristic_filename};
    g -> print_route(origin_city, destination_city);
    return 0;
}