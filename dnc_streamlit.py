import streamlit as st
import pandas as pd
import csv
from io import BytesIO


def read_file(file):
    content = file.getvalue()
    if file.name.endswith('.xlsx'):
        df = pd.read_excel(BytesIO(content))
    elif file.name.endswith('.csv'):
        df = pd.read_csv(BytesIO(content))
    else:
        raise ValueError("Unsupported file type. Please provide a .xlsx or .csv file.")
    return df.values.flatten().tolist()


def check_dnc_number(dnc_set, number_set):
    good_set = number_set - dnc_set
    bad_set = number_set.intersection(dnc_set)
    return good_set, bad_set


def save_to_csv(final_numbers):
    try:
        with open('dnc_scrubbed_numbers.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([[item] for item in final_numbers])

        return 'dnc_scrubbed_numbers.csv'
    except Exception as e:
        st.error(f"Error while saving to CSV: {e}")


def main_dnc():
    st.title('DNC Scrubber Tool')

    st.subheader('Upload DNC File (.xlsx or .csv)')
    dnc_file = st.file_uploader('Choose a DNC file', type=['xlsx', 'csv'], key='dnc_file')

    st.subheader('Upload Data File (.xlsx or .csv)')
    data_file = st.file_uploader('Choose a data file', type=['xlsx', 'csv'], key='data_file')

    if dnc_file and data_file:
        try:
            dnc_set = set(read_file(dnc_file))
            number_set = set(read_file(data_file))

            st.write(f"Total Numbers in your Data file: {len(number_set)}")

            with st.spinner('Scrubbing DNC numbers...'):
                good_set, bad_set = check_dnc_number(dnc_set, number_set)

            st.success("Data scrubbing complete!")
            st.subheader(f"Total Good Numbers Found = ({len(good_set)})")
            st.subheader("Download Scrubbed Data")

            csv_file = save_to_csv(good_set)

            if csv_file:
                with open(csv_file, 'rb') as f:
                    st.download_button(
                        label="Download DNC Scrubbed Numbers",
                        data=f,
                        file_name=csv_file,
                        mime='text/csv',)

            st.success(f"Total DNC Numbers Found and Removed: {len(bad_set)}")

        except Exception as e:
            st.error(f"Error: {e}")


if __name__ == '__main__':
    main_dnc()
