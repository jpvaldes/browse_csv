import pandas as pd

def load_data(data_file):
    try:
        df = pd.read_csv(data_file)
    except Exception as e:
        raise IOError(f'{data_file} not found: {e}')
    df = df.fillna('No Answer')
    return df


def save_decision(output_file, idx, yes, no, na):
    # create this decision
    this_dec = dict(
        idx=idx,
        yes=yes,
        no=no,
        na=na)

    # check if we already have data
    if output_file.exists():
        other_dec = check_idx(output_file, idx)
        dec = pd.concat((other_dec,
                         pd.DataFrame.from_records([this_dec])))
    else:
        dec = pd.DataFrame.from_records([this_dec])

    # save what we have
    try:
        dec.to_csv(output_file, index=False)
    except Exception as e:
        raise IOError(f'{e}')


def check_idx(output_file, idx):
    """
    Remove row if entry corresponding to idx already existed

    That means the user can change her/his mind also about an entry
    """
    df = pd.read_csv(output_file)
    df = df[~df.idx.isin([idx])]
    return df
