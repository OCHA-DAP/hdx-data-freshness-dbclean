from os import remove
from os.path import join
from shutil import copyfile

import pytest
from dbactions.dbclean import DBClean
from hdx.database import Database
from hdx.utilities.compare import assert_files_same
from hdx.utilities.dateparse import parse_date
from hdx.utilities.path import temp_dir


class TestDBClean:
    @pytest.fixture(scope="class")
    def fixtures(self):
        return join("tests", "fixtures")

    @pytest.fixture(scope="function")
    def database(self, fixtures):
        dbfile = "test_freshness.db"
        dbpath = join("tests", dbfile)
        try:
            remove(dbpath)
        except FileNotFoundError:
            pass
        copyfile(join(fixtures, dbfile), dbpath)
        return {"dialect": "sqlite", "database": dbpath}

    def test_clean(self, database, fixtures):
        with temp_dir(
            "test_dbclean", delete_on_success=True, delete_on_failure=False
        ) as folder:
            with Database(**database) as session:
                cleaner = DBClean(session)

                def check_results(
                    runs_file,
                    date_str,
                    exp_starting_runs,
                    exp_runs=None,
                    exp_success=True,
                    check_enddate=True,
                ):
                    expected_runs = join(fixtures, runs_file)
                    actual_runs = join(folder, runs_file)
                    starting_runs = cleaner.get_runs()
                    assert len(starting_runs) == exp_starting_runs

                    now = parse_date(date_str)
                    success = cleaner.run(
                        now, check_enddate=check_enddate, filepath=actual_runs
                    )
                    assert success is exp_success
                    if not success:
                        return
                    runs = cleaner.get_runs()
                    assert len(runs) == exp_runs
                    assert_files_same(actual_runs, expected_runs)

                check_results("runs.csv", "2023-02-27", 2072, 898)
                check_results("runs2.csv", "2023-02-28", 898, 897)
                check_results("runs3.csv", "2023-03-01", 897, 897)
                check_results("runs3.csv", "2023-03-06", 897, exp_success=False)
                check_results("runs3.csv", "2023-03-06", 897, 897, check_enddate=False)
                check_results("runs4.csv", "2023-03-07", 897, 895, check_enddate=False)
                check_results("runs5.csv", "2023-04-01", 895, 874, check_enddate=False)
