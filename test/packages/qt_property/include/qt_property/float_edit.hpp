//
//   Copyright 2026 R. Kent James <kent@caspia.com>
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

#ifndef QT_PROPERTY__FLOAT_EDIT_HPP_
#define QT_PROPERTY__FLOAT_EDIT_HPP_

#include <QLineEdit>

namespace qt_property
{

/// A line edit holding a float, exposed to Qt as a Q_PROPERTY.
class FloatEdit : public QLineEdit
{
  Q_OBJECT
  /// The float value shown in the editor.
  Q_PROPERTY(float value READ getValue WRITE setValue USER true)

public:
  explicit FloatEdit(QWidget * parent = 0);

  /// Get the current value.
  float getValue();

  /// Set the current value.
  void setValue(float new_value);
};

}  // namespace qt_property

#endif  // QT_PROPERTY__FLOAT_EDIT_HPP_
