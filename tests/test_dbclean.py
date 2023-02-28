from os import remove
from os.path import join
from shutil import copyfile

import pytest
from dbclean import DBClean
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
                runs_file = "runs.csv"
                expected_runs = join(fixtures, runs_file)
                actual_runs = join(folder, runs_file)
                now = parse_date("2023-02-27")
                cleaner = DBClean(session, now)
                starting_runs = cleaner.get_runs()
                assert len(starting_runs) == 2072
                success = cleaner.clean(filepath=actual_runs)
                assert success is True
                runs = cleaner.get_runs()
                assert len(runs) == 898
                assert_files_same(actual_runs, expected_runs)

                runs_file = "runs2.csv"
                expected_runs = join(fixtures, runs_file)
                actual_runs = join(folder, runs_file)
                now = parse_date("2023-02-28")
                cleaner = DBClean(session, now)
                starting_runs = cleaner.get_runs()
                assert len(starting_runs) == 898
                success = cleaner.clean(filepath=actual_runs)
                assert success is True
                runs = cleaner.get_runs()
                assert len(runs) == 897
                assert_files_same(actual_runs, expected_runs)

                runs_file = "runs3.csv"
                expected_runs = join(fixtures, runs_file)
                actual_runs = join(folder, runs_file)
                now = parse_date("2023-03-01")
                cleaner = DBClean(session, now)
                starting_runs = cleaner.get_runs()
                assert len(starting_runs) == 897
                success = cleaner.clean(filepath=actual_runs)
                assert success is True
                runs = cleaner.get_runs()
                assert len(runs) == 897
                assert_files_same(actual_runs, expected_runs)

                now = parse_date("2023-03-06")
                cleaner = DBClean(session, now)
                starting_runs = cleaner.get_runs()
                assert len(starting_runs) == 897
                success = cleaner.clean(filepath=actual_runs)
                assert success is False

                success = cleaner.clean(check_enddate=False, filepath=actual_runs)
                assert success is True
                runs = cleaner.get_runs()
                assert len(runs) == 897
                assert_files_same(actual_runs, expected_runs)

                runs_file = "runs4.csv"
                expected_runs = join(fixtures, runs_file)
                actual_runs = join(folder, runs_file)
                now = parse_date("2023-03-07")
                cleaner = DBClean(session, now)
                starting_runs = cleaner.get_runs()
                assert len(starting_runs) == 897
                success = cleaner.clean(check_enddate=False, filepath=actual_runs)
                assert success is True
                runs = cleaner.get_runs()
                assert len(runs) == 895
                assert_files_same(actual_runs, expected_runs)

                runs_file = "runs5.csv"
                expected_runs = join(fixtures, runs_file)
                actual_runs = join(folder, runs_file)
                now = parse_date("2023-04-01")
                cleaner = DBClean(session, now)
                starting_runs = cleaner.get_runs()
                assert len(starting_runs) == 895
                success = cleaner.clean(check_enddate=False, filepath=actual_runs)
                assert success is True
                runs = cleaner.get_runs()
                assert len(runs) == 874
                assert_files_same(actual_runs, expected_runs)
