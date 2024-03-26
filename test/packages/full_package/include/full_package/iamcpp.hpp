//
//   Copyright 2022 R. Kent James <kent@caspia.com>
//
//   Licensed under the Apache License, Version 2.0 (the "License");
//   you may not use this file except in compliance with the License.
//   You may obtain a copy of the License at
//
//       http://www.apache.org/licenses/LICENSE-2.0
//
//   Unless required by applicable law or agreed to in writing, software
//   distributed under the License is distributed on an "AS IS" BASIS,
//   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//   See the License for the specific language governing permissions and
//   limitations under the License.

#ifndef FULL_PACKAGE__IAMCPP_HPP_
#define FULL_PACKAGE__IAMCPP_HPP_

/// @file
/// @brief This is the header file for the DoSomeCpp class implementing a node do_some_cpp

#include <tuple>
#include "rclcpp/rclcpp.hpp"

/// namespace for the ROS2 package containing the do_some_cpp node
namespace full_package
{

/**

  A demonstration of a simple ROS2 node that does nothing.

  <b>Bold Statement</b> Describe that boldness

  Just plain old documentation.

  */

class DoSomeCpp: public rclcpp::node
{
public:
  DoSomeCpp();
  virtual ~DoSomeCpp() {}

  /// Generate the root and power of a number
  static std::tuple<double, double> apply_powers(
    const double_t number,  ///< base value we want to take to a power or root
    const double exponent   ///< the exponent for the power or root
  );

  /// here I document some variable

  size_t count
};

}  // namespace full_package

#endif  // FULL_PACKAGE__IAMCPP_HPP_
