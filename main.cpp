#include <iostream>
#include <string>
#include <bitset>
#include <vector>
#include <cmath>
#include <pqxx/pqxx>
#include "matplotlibcpp.h"

enum shape { point=1, line=2, polygon=3 };

// little endian hex to double
double hextodouble (std::string&& val) {
  // todo: not 100% accurate

  int sign;
  int exponent;
  long long mantissa;
  double res;

  // convert little endian to big 
  for (int i = 14; i >= 0; i -= 2) {
    if (i == 14) { 
      sign = std::stoi(val.substr(i, 2),0 , 16) & 0x80;
      exponent = (std::stoi(val.substr(i, 2),0 , 16) & 0x7f) << 4;
    } else if (i == 12) {
      exponent |= (std::stoi(val.substr(i, 2),0 , 16) & 0xf0) >> 4;
      exponent -= 1023;
      mantissa = std::stoi(val.substr(i, 2),0 , 16) & 0x0f;
    } else {
      mantissa <<= 8;
      mantissa |= std::stoi(val.substr(i, 2),0 , 16);
    }
  }

  // calculate mantissa
  for (int i = 0; i < 52; i++) 
    if ((mantissa & 1ll << i) >> i) 
      res += 1 / std::pow(2, i+1);
  res += 1;
  // handle exponent
  res *= std::pow(2, exponent);
  // handle sign
  if (sign) res *= -1;

  return res;
}


void plotobj(std::string&& num) {
  
  int start;
  int type = std::stoi(num.substr(2,2), 0, 16);

  // point coords
  std::vector<double> x;
  std::vector<double> y;

  // type
  switch(type) { 
    case point: start = 18; break;
    case line: start = 26; break;
    case polygon: start = 32; break;
  }

  // add coords to vector
  for (int i = start; i < num.size(); i += 16) {
    if (((i-start)/32) % 2 != 0 || (i-start) == 0) 
      x.push_back(hextodouble(num.substr(i, 16)));
    else
      y.push_back(hextodouble(num.substr(i, 16)));
  } 

  // plot
  if (type == point) 
    matplotlibcpp::plot(x,y,"bo");
  else
    matplotlibcpp::plot(x,y,"bo-");
}


int main() {

  try {
    pqxx::connection c("host=localhost port=5432 dbname=osm user=postgres password=password");
    pqxx::work w(c);
    pqxx::result r = w.exec("select way from planet_osm_point limit 10");
    w.commit();
    
    // convert geometry objects
    for (size_t i=0; i < r.size(); i++)
      plotobj(r[i][0].c_str());

  } catch (const std::exception& e) {
    std::cerr << e.what() << std::endl;
    return 1;
  }

  matplotlibcpp::show();
}

