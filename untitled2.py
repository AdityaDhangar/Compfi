# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CFVNzHIb_cFpAG3oL0Li3r8tPpqMKEbU
"""

import requests
from bs4 import BeautifulSoup
from statistics import mean
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract data (replace this with the actual HTML structure of the websites)
        offers_data = float(soup.find('div', class_='last-offer').text.strip('%').replace(',', '')) if soup.find('div', class_='offers') else None
        satisfaction_data = float(soup.find('div', class_='transaction-status').text) if soup.find('span', class_='user-satisfaction') else None
        transactions_data = float(soup.find('div', class_='successful-transactions').text.replace('Transactions:', '').strip()) if soup.find('div', class_='successful-transactions') else None

        return {
            'offers': offers_data,
            'satisfaction': satisfaction_data,
            'transactions': transactions_data
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Example URLs (replace these with the actual URLs of the websites)
website1_url = 'https://6566bf0d5c139716fc22ff8b--luxury-narwhal-b165e1.netlify.app/'
website2_url = 'https://6566bf7d777302174352174c--grand-youtiao-e32227.netlify.app/'
website3_url = 'https://6566bf40f7136e17596958e7--joyful-sopapillas-478785.netlify.app/'
your_application_url = 'https://6566bf848d605917eeded57c--radiant-paprenjak-760fb0.netlify.app/'

# Scrape data for each website
data_website1 = scrape_website('https://6566bf0d5c139716fc22ff8b--luxury-narwhal-b165e1.netlify.app/')
data_website2 = scrape_website('https://6566bf7d777302174352174c--grand-youtiao-e32227.netlify.app/')
data_website3 = scrape_website('https://6566bf40f7136e17596958e7--joyful-sopapillas-478785.netlify.app/')
your_application_data = scrape_website('https://6566bf848d605917eeded57c--radiant-paprenjak-760fb0.netlify.app/')

# Compare websites based on different parameters
offers_comparison = max([(data_website1['offers'], 'Website 1'), (data_website2['offers'], 'Website 2'), (data_website3['offers'], 'Website 3')])
satisfaction_comparison = max([(data_website1['satisfaction'], 'Website 1'), (data_website2['satisfaction'], 'Website 2'), (data_website3['satisfaction'], 'Website 3')])
transactions_comparison = max([(data_website1['transactions'], 'Website 1'), (data_website2['transactions'], 'Website 2'), (data_website3['transactions'], 'Website 3')])

# Output the best website in each category
print(f"Best website for offers: {offers_comparison[1]} with {offers_comparison[0]}% offers")
print(f"Best website for user satisfaction: {satisfaction_comparison[1]} with {satisfaction_comparison[0]} rating")
print(f"Best website for transactions: {transactions_comparison[1]} with {transactions_comparison[0]} transactions")

# Compare your application with the best website parameters
if your_application_data:
    print("\nComparison with Your Application:")
    for parameter in ['offers', 'satisfaction', 'transactions']:
        your_value = your_application_data[parameter]
        best_value = 0

        print(f"Your application's {parameter}: {your_value}")
        print(f"Best website's {parameter}: {best_value}")

        if your_value is not None and best_value is not None:
            if your_value >= best_value:
                print(f"Your application has a higher {parameter} compared to the best website.")
            else:
                print(f"Your application has a lower {parameter} compared to the best website.")
        else:
            print(f"Cannot compare {parameter} due to missing data.")
else:
    print("\nError scraping data for your application.")

# Recommendation logic
# Recommendation logic
if your_application_data:
    overall_score = mean([your_application_data['offers'], your_application_data['satisfaction'], your_application_data['transactions']])
    best_overall_score = max(mean(data_website1.values()), mean(data_website2.values()), mean(data_website3.values()))

    if overall_score >= best_overall_score:
        print("\nRecommendation: Your application is recommended based on the comparison.")
    else:
        print("\nRecommendation: Your application is not recommended based on the comparison.")
else:
    print("\nCannot provide a recommendation due to missing data for your application.")


# Machine Learning using Linear Regression
if your_application_data:
    # Features (X) and Target variable (y)
    features = ['offers', 'satisfaction']
    X = pd.DataFrame({feature: [data_website1[feature], data_website2[feature], data_website3[feature]] for feature in features})
    y = pd.DataFrame({'transactions': [data_website1['transactions'], data_website2['transactions'], data_website3['transactions']]})

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions on the testing set
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    print(f'\nMean Squared Error for Transaction Prediction: {mse}')
else:
    print("\nCannot perform machine learning due to missing data for your application.")