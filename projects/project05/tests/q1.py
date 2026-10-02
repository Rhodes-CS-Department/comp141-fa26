test = {
  'name': 'Question 1',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> from tanchi_boska import *

          >>> score(5, 5, 5)
          30
          
          >>> score(10, 0, 10)
          10
          
          >>> score(0, 10, 10)
          100
          
          >>> score(1, 4, 6)
          25
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
