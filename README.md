Py-Roma
----

This package provides handy tools for regular development in python.

> At the heart of the conquest of Rome's vast territory was a sophisticated 
  infrastructure.

- [console](##console)
    - [Fancy Text](###fancy-text)
    - [Progress Bar](###progress-bar)
- [spqr](##spqr)
    - [censor](###censor)
    - [atticus](###atticus)

## `console`  
`console` should be imported in the manner below:

```python
from roma import console
```

### Fancy Text
Demo:
```python
console.write_line('#{Hello}{red} #{World}{blue}!')
```

### Progress Bar
Demo:
```python
import time

total = 100
quarter = int(total / 4)
for i in range(1, total + 1):
  if i % quarter == 0:
    console.write_line('{}/{} done!'.format(i, total))
  console.print_progress(i, total)
  time.sleep(0.05)
```

## `spqr`
This package serves as a MISC package, which contains a bundle of common, useful tools.

### `censor`

`censor` module handles issues related to argument types.

Demo of `check_type()`:
```python
from roma import censor

assert all([
  censor.check_type(31, int) == 31,
  censor.check_type({'adh', 93, 19}, inner_type=str) 
    == {'adh', '93', '19'},
  censor.check_type([None, 12, 19.0], tuple, 
    inner_type=int, nullable=True) == (None, 12, 19),
])

```

### `atticus`

`atticus` provides tools for produce appropriate strings.

Demo of `ordinal()`:
```python
from roma import atticus

assert all([
  atticus.ordinal(1) == '1st', atticus.ordinal(2) == '2nd', atticus.ordinal(3) == '3rd',
  atticus.ordinal(8) == '8th', atticus.ordinal(11) == '11th', atticus.ordinal(12) == '12th',
  atticus.ordinal(13) == '13th', atticus.ordinal(21) == '21st', atticus.ordinal(112) == '112th',
])
```

