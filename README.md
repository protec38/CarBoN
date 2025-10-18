# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/protec38/CarBoN/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                                                      |    Stmts |     Miss |   Cover |   Missing |
|------------------------------------------------------------------------------------------ | -------: | -------: | ------: | --------: |
| main/\_\_init\_\_.py                                                                      |        0 |        0 |    100% |           |
| main/admin.py                                                                             |       45 |        4 |     91% |13, 54, 74-84 |
| main/apps.py                                                                              |        4 |        0 |    100% |           |
| main/forms.py                                                                             |       42 |        0 |    100% |           |
| main/migrations/0001\_initial.py                                                          |        6 |        0 |    100% |           |
| main/migrations/0002\_defect\_reporter\_name\_alter\_defect\_solution\_date\_and\_more.py |        4 |        0 |    100% |           |
| main/migrations/0003\_alter\_defect\_reporter\_name\_alter\_vehicle\_type.py              |        4 |        0 |    100% |           |
| main/migrations/0004\_vehicle\_mileage\_trip.py                                           |        6 |        0 |    100% |           |
| main/migrations/0005\_rename\_carburant\_vehicle\_fuel\_and\_more.py                      |        4 |        0 |    100% |           |
| main/migrations/0006\_fuelexpense.py                                                      |        6 |        0 |    100% |           |
| main/migrations/0007\_alter\_fuelexpense\_options\_alter\_fuelexpense\_vehicle.py         |        5 |        0 |    100% |           |
| main/migrations/0008\_alter\_location\_options\_alter\_fuelexpense\_amount\_and\_more.py  |        5 |        0 |    100% |           |
| main/migrations/0009\_alter\_vehicle\_parking\_location.py                                |        5 |        0 |    100% |           |
| main/migrations/0010\_setting.py                                                          |        5 |        0 |    100% |           |
| main/migrations/0010\_vehicle\_inventory.py                                               |        4 |        0 |    100% |           |
| main/migrations/0011\_merge\_0010\_setting\_0010\_vehicle\_inventory.py                   |        4 |        0 |    100% |           |
| main/migrations/0012\_fuelexpense\_form\_of\_payment.py                                   |        4 |        0 |    100% |           |
| main/migrations/\_\_init\_\_.py                                                           |        0 |        0 |    100% |           |
| main/models.py                                                                            |      154 |        5 |     97% |60, 146, 149, 277, 290 |
| main/tests/\_\_init\_\_.py                                                                |        0 |        0 |    100% |           |
| main/tests/test\_defects.py                                                               |       30 |        0 |    100% |           |
| main/tests/test\_fuel\_expense.py                                                         |       17 |        0 |    100% |           |
| main/tests/test\_trips.py                                                                 |       95 |        0 |    100% |           |
| main/urls.py                                                                              |        3 |        0 |    100% |           |
| main/utils.py                                                                             |       15 |        0 |    100% |           |
| main/views.py                                                                             |      118 |       27 |     77% |30-80, 154-156, 219-221 |
| settings/\_\_init\_\_.py                                                                  |        0 |        0 |    100% |           |
| settings/settings.py                                                                      |       18 |        0 |    100% |           |
| settings/urls.py                                                                          |        4 |        0 |    100% |           |
|                                                                                 **TOTAL** |  **607** |   **36** | **94%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/protec38/CarBoN/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/protec38/CarBoN/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/protec38/CarBoN/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/protec38/CarBoN/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fprotec38%2FCarBoN%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/protec38/CarBoN/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.