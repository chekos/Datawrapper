# History

## 0.0.7 (2020-06-23)
- fixes bug where `_check_data_folder()` would ignore the `path` parameter
- uses `path.mkdir(..., exists_ok=True)` now
- adds 2018 to possible survey years
- first contributor! [@yonran](https://github.com/yonran) 🎉

## 0.0.6 (2020-05-23)
- Bug fixes (some url's at the census website didn't have `content-size`, switched to default dict to move past that case)

## 0.0.5 (2019-05-11)
- Add `.as_dataframe()` to ACS class. 

## 0.0.4 (2019-05-10)
- Add `.download_data()` to ACS class. 

## 0.0.3 (2019-05-09)
- Accidentally released lol

## 0.0.2 (2019-05-09)
- Add `ACS()` class for python interface.

## 0.0.1 (2019-04-29)
-  First release on PyPI.
