test = {
  'name': 'Question 1',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> from cs1.notebooks import *
          >>> reload_functions("imgfilter.py")
          >>> make_output_filename("lynx.ppm", 1)
          'lynx_negate_red.ppm'
          >>> make_output_filename("rhodes.ppm", 9)
          'rhodes_grayscale.ppm'
          >>> make_output_filename("bclc.ppm", 5)
          'bclc_remove_red.ppm'
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
