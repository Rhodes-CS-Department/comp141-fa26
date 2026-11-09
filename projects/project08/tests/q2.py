test = {
  'name': 'Question 2',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> from cs1.notebooks import *
          >>> reload_functions("imgfilter.py")
          >>> negate([0, 1, 2, 3, 4, 5, 200, 201, 202, 203, 255])
          [255, 254, 253, 252, 251, 250, 55, 54, 53, 52, 0]
          >>> flatten([1])
          [0]
          >>> flatten([1, 2, 2, 3, 4, 4, 4, 4])
          [0, 0, 0, 0, 0, 0, 0, 0]
          >>> flip([1])
          [1]
          >>> flip([1, 2])
          [2, 1]
          >>> flip([1, 2, 3, 4])
          [4, 3, 2, 1]
          >>> grayscale([1, 10, 100], [0, 20, 50], [2, 0, 0])
          [1, 10, 50]
          """,
          'hidden': False,
          'locked': False,
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
