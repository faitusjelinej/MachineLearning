import pandas as pd

def format_uk_phone(phone):
    if pd.isna(phone):
        return None
    phone = str(phone).replace(" ", "").strip()
    if len(phone) >= 10:
        last_10 = phone[-10:]
        return f"+44{last_10}"
    
file_path = "QUB_Analytathon2_Deloitte_data.csv"
df = pd.read_csv(file_path)
print("Total number of records in the QUB_Analytathon2_Deloitte_data.csv", len(df))
# df = df.fillna('Not Available').replace('', 'Not Available')

print('Remove rows that are duplicates in all columns.')
df = df.drop_duplicates()
print("Total number of records after", len(df))

print('Make all the phone numbers in same format +44XXXXXXXXXX and remove duplicates.')
df['phone'] = df['phone_number'].apply(format_uk_phone)
df = df.drop(columns=['phone_number'])
df_sorted = df.sort_values(by=['first_name', 'middle_name','last_name'], ascending=[True, True, True])
df_sorted.to_csv("sorted_data.csv", index=False)
df = df_sorted.drop_duplicates()
print("Total number of records after", len(df))

print("Merge records with same details but one record with Address blank")
df_cleaned = (
    df.sort_values(
        by=['house_no', 'primary_street', 'town', 'postcode', 'county'], 
        na_position='last'
    )
    .drop_duplicates(
        subset=['prefix', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'email_address', 'phone'], 
        keep='first'
    )
    .reset_index(drop=True)
            )
print("Total number of records after", len(df_cleaned))


print("Merge records with same details but one record with date_of_birth blank")
df_cleaned = (
    df_cleaned.sort_values(
        by=['date_of_birth'], 
        na_position='last'
    )
    .drop_duplicates(
        subset=['prefix', 'first_name', 'middle_name', 'last_name', 'email_address','house_no','primary_street','town','postcode','county','phone'], 
        keep='first'
    )
    .reset_index(drop=True)
            )
print("Total number of records after", len(df_cleaned))

print("Merge records with same details but one record with phone number blank")
df_cleaned = (
    df_cleaned.sort_values(
        by=['phone'], 
        na_position='last'
    )
    .drop_duplicates(
        subset=['prefix', 'first_name', 'middle_name', 'last_name','date_of_birth' ,'email_address','house_no','primary_street','town','postcode','county'], 
        keep='first'
    )
    .reset_index(drop=True)
            )
print("Total number of records after", len(df_cleaned))

print("Merge records with same details but one record with email address blank")
df_cleaned = (
    df_cleaned.sort_values(
        by=['email_address'], 
        na_position='last'
    )
    .drop_duplicates(
        subset=['prefix', 'first_name', 'middle_name', 'last_name' ,'date_of_birth','house_no','primary_street','town','postcode','county','phone'], 
        keep='first'
    )
    .reset_index(drop=True)
            )
print("Total number of records after", len(df_cleaned))

print("Merge records with typo in first_name")
key_columns = ['prefix', 'middle_name', 'last_name', 'date_of_birth', 'email_address','house_no', 
               'primary_street', 'town', 'postcode', 'county', 'phone']

df_cleaned = df_cleaned.drop_duplicates(subset=key_columns, keep='first')

print("Total number of records after", len(df_cleaned))

print("Merge records with typo in middle_name")
key_columns = ['prefix', 'first_name', 'last_name', 'date_of_birth', 'email_address','house_no', 
               'primary_street', 'town', 'postcode', 'county', 'phone']

df_cleaned = df_cleaned.drop_duplicates(subset=key_columns, keep='first')

print("Total number of records after", len(df_cleaned))

print("Merge records with typo in last_name")
key_columns = ['prefix', 'first_name', 'middle_name', 'date_of_birth', 'email_address','house_no', 
               'primary_street', 'town', 'postcode', 'county', 'phone']

df_cleaned = df_cleaned.drop_duplicates(subset=key_columns, keep='first')

print("Total number of records after", len(df_cleaned))

print("Merge records with same details but one record with Address and Phone blank")
df_cleaned = (
    df_cleaned.sort_values(
        by=['house_no', 'primary_street', 'town', 'postcode', 'county','phone'], 
        na_position='last'
    )
    .drop_duplicates(
        subset=['prefix', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'email_address'], 
        keep='first'
    )
    .reset_index(drop=True)
            )
print("Total number of records after", len(df_cleaned))

print("Merge records with same details but one record with email address")

df_cleaned = (
    df_cleaned.sort_values(
        by=['email_address'], 
        na_position='last'
    )
    .drop_duplicates(
        subset=['prefix',  'middle_name', 'last_name', 'date_of_birth','house_no', 'primary_street', 'town', 'postcode', 'county','phone'], 
        keep='first'
    )
    .reset_index(drop=True)
            )

print("Total number of records after", len(df_cleaned))

print("Merge records with same prefix, name, DOB , phone. Address is blank. email different. Separated by comma.")

def pick_first(series):
    return series.dropna().iloc[0] if not series.dropna().empty else None

df_cleaned = (
    df_cleaned.groupby(['prefix', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'phone'], dropna=False)
    .agg({
        'email_address': lambda x: ', '.join(sorted(set(x.dropna()))),
        'house_no': pick_first,
        'primary_street': pick_first,
        'town': pick_first,
        'postcode': pick_first,
        'county': pick_first
    })
    .reset_index()
)

print("Total number of records after", len(df_cleaned))

print("Merge records with same prefix, name, DOB , phone and address. Email and Phone blank in one record")

df_cleaned = (
    df_cleaned.groupby(['prefix', 'first_name', 'middle_name', 'last_name', 'date_of_birth','house_no','primary_street','town','postcode','county'], dropna=False)
    .agg({
        'email_address': pick_first,
        'phone': pick_first
    })
    .reset_index()
)

print("Total number of records after", len(df_cleaned))


print("Merge records with same prefix, first_name,last_name, DOB, phone and address. Email & Phone blank in one record")

df_cleaned = (
    df_cleaned.groupby(['prefix', 'first_name', 'last_name', 'date_of_birth','house_no','primary_street','town','postcode','county'], dropna=False)
    .agg({
        'email_address': pick_first,
        'phone': pick_first,
        'middle_name': pick_first
    })
    .reset_index()
)

print("Total number of records after", len(df_cleaned))

print("Remove rows with only prefix, first_name,middle_name,last_name and other details blank.")


columns_to_check = ['prefix', 'first_name', 'middle_name', 'last_name']
columns_to_check_blank = ['date_of_birth', 'house_no', 'primary_street', 'town', 'postcode', 'county','phone']


all_columns = df_cleaned.columns.tolist()
other_columns = [col for col in all_columns if col not in columns_to_check]
df_cleaned = df_cleaned[~df_cleaned[columns_to_check_blank].isna().all(axis=1)]

print("Total number of records after", len(df_cleaned))

print("Merge records with same prefix, name, Address. DOB blank in one record. email different. Separated by comma.")

df_cleaned = (
    df_cleaned.groupby(['prefix', 'first_name', 'middle_name', 'last_name', 'phone', 'house_no', 'primary_street', 'town', 'postcode', 'county'], dropna=False)
    .agg({
        'email_address': lambda x: ', '.join(sorted(set(x.dropna()))),
        'date_of_birth': pick_first
    })
    .reset_index()
)
print("Total number of records after", len(df_cleaned))

print("Merge records with same prefix, first_name,middle_name,last_name and phone. Other fields blank in one record")

df_cleaned = (
    df_cleaned.groupby(['prefix', 'first_name','middle_name' ,'last_name', 'phone'], dropna=False)
    .agg({
        'email_address': pick_first,
        'date_of_birth': pick_first,
        'house_no': pick_first, 
        'primary_street': pick_first, 
        'town': pick_first, 
        'postcode': pick_first, 
        'county': pick_first
    })
    .reset_index()
)

print("Total number of records after", len(df_cleaned))

print("Merge records with same prefix, name, Address. DOB and Phone blank in one record. Email different. Separated by comma.")

df_cleaned = (
    df_cleaned.groupby(['prefix', 'first_name', 'middle_name', 'last_name', 'house_no', 'primary_street','town','postcode','county'], dropna=False)
    .agg({
        'email_address': lambda x: ', '.join(sorted(set(x.dropna()))),
         'phone': pick_first,
         'date_of_birth': pick_first
    })
    .reset_index()
)

print("Total number of records after", len(df_cleaned))

df_sorted = df_cleaned.sort_values(by=['first_name', 'middle_name','last_name'], ascending=[True, True, True])
df_sorted.to_csv("formatted_data.csv", index=False)
print("Saved to 'formatted_data.csv'")




