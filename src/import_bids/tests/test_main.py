import pytest

from import_bids import main

@pytest.mark.parametrize("option", (""))
def test_no_args(capsys, option):

    with pytest.raises(SystemExit):
        main(option)

    out = capsys.readouterr().out
    assert "import-bids: error: the following arguments are required: raw_dir, bids_dir, task" in out

@pytest.mark.parametrize("option", ("-h", "--help"))
def test_help(capsys, option):

    with pytest.raises(SystemExit):
        main(option)

    out = capsys.readouterr().out
    assert "usage: import-bids" in out

@pytest.mark.parametrize("option", ("data/input/raw data/bids-out 01 --dryrun",))
def test_basic(capsys, option):

    with pytest.raises(SystemExit):
        main(option)

    out = capsys.readouterr().out
    assert "import-bids: error: the following arguments are required: raw_dir, bids_dir, task" in out