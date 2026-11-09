test = {
  'name': 'Question 3',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> from cs1.notebooks import *
          >>> reload_functions("imgfilter.py")
          >>> get_channel(["1", "2", "3", "4", "5", "6"], 0)
          [1, 4]
          >>> get_channel(["1", "2", "3", "4", "5", "6"], 1)
          [2, 5]
          >>> get_channel(["1", "2", "3", "4", "5", "6"], 2)
          [3, 6]
          >>> get_channel(["255", "0", "10"], 2)
          [10]
          >>> make_line([1, 2, 3])
          '1 2 3 '
          >>> make_line([255])
          '255 '
          >>> make_line([0, 0, 10, 255, 128, 20])
          '0 0 10 255 128 20 '
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
