## Configuration is entered at the top of the file like this**

# SETUP

Supports: 1, 2, 3
`n_circles = 3`

Set to True if you want the circle to be labelled
`to_label = [ 
  ["c1", True],
  ["c2", True],
  ["c3", False],
  ["c1c2", False],
  ["c1c3", False],
  ["c2c3", False],
  ["c1c2c3", True],
] `

Set the text to be displayed by the key, set to `None` for no text
`key_label = " = selected area"`

Size of the window
`WIN_WIDTH = 1600
WIN_HEIGHT = 1600`

Choose between `'sharp'` and `'fast'` - `sharp` will run fast unless using a high screen resolution ~1440p or 2160p onwards
`draw_mode = 'sharp'`


# END SETUP
