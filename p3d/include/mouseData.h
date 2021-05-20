/**
 * PANDA 3D SOFTWARE
 * Copyright (c) Carnegie Mellon University.  All rights reserved.
 *
 * All use of this software is subject to the terms of the revised BSD
 * license.  You should have received a copy of this license along
 * with this source code in a file named "LICENSE."
 *
 * @file mouseData.h
 * @author drose
 * @date 1999-02-08
 */

#ifndef MOUSEDATA_H
#define MOUSEDATA_H

#include "pandabase.h"

#include "modifierButtons.h"

/**
 * Holds the data that might be generated by a 2-d pointer input device, such
 * as the mouse in the GraphicsWindow.
 */
class EXPCL_PANDA_PUTIL MouseData {
PUBLISHED:
  INLINE MouseData();
  INLINE MouseData(const MouseData &copy);
  INLINE void operator = (const MouseData &copy);

  INLINE double get_x() const;
  INLINE double get_y() const;
  INLINE bool get_in_window() const;

  void output(ostream &out) const;

  MAKE_PROPERTY(x, get_x);
  MAKE_PROPERTY(y, get_y);
  MAKE_PROPERTY(in_window, get_in_window);

public:
  bool _in_window;
  double _xpos;
  double _ypos;
};

INLINE ostream &operator << (ostream &out, const MouseData &md);

#include "mouseData.I"

#endif