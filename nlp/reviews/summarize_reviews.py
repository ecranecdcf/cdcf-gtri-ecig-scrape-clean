import pandas as pd
import matplotlib.pyplot as plt 

csv_file = 'nlp/reviews/results/iced_reviews_v4.csv'

df = pd.read_csv(csv_file)

cols = ['Product', 'Review', 'Review Indicated Iced', 'Review Justification',
       'Site', 'Product ID', 'Review ID', 'Sweet Level', 'Iced Level',
       'Rating']

# Group by Review Indicated Iced and count
summary = df.groupby('Review Indicated Iced').size().reset_index(name='Count')
print(summary)

# percetage True vs False
total = len(df)
true_count = summary[summary['Review Indicated Iced'] == True]['Count'].values
false_count = summary[summary['Review Indicated Iced'] == False]['Count'].values    
true_count = true_count[0] if len(true_count) > 0 else 0
false_count = false_count[0] if len(false_count) > 0 else 0
true_percentage = (true_count / total) * 100
false_percentage = (false_count / total) * 100  
print(f"Total Reviews: {total}")
print(f"True: {true_count} ({true_percentage:.2f}%)")
print(f"False: {false_count} ({false_percentage:.2f}%)")        

# do the same, grouping by product
product_summary = df.groupby(['Product', 'Review Indicated Iced']).size().reset_index(name='Count')
print(product_summary)
# for each product, calculate the percentage of at least one positive review
# i.e., Review Indicated Iced == True
products = df['Product'].unique()
product_positive_summary = []
for product in products:
    product_df = df[df['Product'] == product]
    total_reviews = len(product_df)
    positive_reviews = len(product_df[product_df['Review Indicated Iced'] == True])
    positive_percentage = (positive_reviews / total_reviews) * 100 if total_reviews > 0 else 0
    product_positive_summary.append({
        'Product': product,
        'Total Reviews': total_reviews,
        'Positive Reviews': positive_reviews,
        'Positive Percentage': positive_percentage
    })
product_positive_df = pd.DataFrame(product_positive_summary)

# get products with at least one positive review
products_with_positive = product_positive_df[product_positive_df['Positive Reviews'] > 0]
sorted_pwp = (products_with_positive.sort_values(by='Positive Percentage', ascending=False))     

# total products
total_products = len(products)
products_with_positive_count = len(products_with_positive)
products_with_positive_percentage = (products_with_positive_count / total_products) * 100 if total_products > 0 else 0
print(f"Total Products: {total_products}")
print(f"Products with at least one positive review: {products_with_positive_count} ({products_with_positive_percentage:.2f}%)")

# summarize iced level vs positive reviews
iced_level_summary = df.groupby(['Iced Level', 'Review Indicated Iced']).size().reset_index(name='Count')
#print(iced_level_summary)   

# plot iced level vs positive reviews
iced_level_pivot = iced_level_summary.pivot(index='Iced Level', columns='Review Indicated Iced', values='Count').fillna(0)
iced_level_pivot.plot(kind='bar', stacked=True)
plt.title('Iced Level vs Review Indicated Iced')
plt.xlabel('Iced Level')
plt.ylabel('Count')
plt.legend(title='Review Indicated Iced', labels=['False', 'True'])
plt.tight_layout()
plt.savefig('nlp/reviews/results/iced_level_vs_review_indicated_iced.png')
plt.close()


# plot overall distribution of iced levels
iced_level_counts = df['Iced Level'].value_counts().sort_index()
iced_level_counts.plot(kind='bar')
plt.title('Overall Distribution of Iced Levels')
plt.xlabel('Iced Level')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('nlp/reviews/results/overall_iced_level_distribution.png')
plt.close()

# plot review indicated iced
review_indicated_iced_counts = df['Review Indicated Iced'].value_counts()
review_indicated_iced_counts.plot(kind='bar')
plt.title('Distribution of Review Indicated Iced')
plt.xlabel('Review Indicated Iced')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('nlp/reviews/results/review_indicated_iced_distribution.png')
plt.close()

#plot rating vs review indicated iced with labels
rating_summary = df.groupby(['Rating', 'Review Indicated Iced']).size().reset_index(name='Count')
rating_pivot = rating_summary.pivot(index='Rating', columns='Review Indicated Iced', values='Count').fillna(0)
rating_pivot.plot(kind='bar', stacked=True)
plt.title('Rating vs Review Indicated Iced')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.legend(title='Review Indicated Iced', labels=['False', 'True'])



plt.tight_layout()
plt.savefig('nlp/reviews/results/rating_vs_review_indicated_iced.png')
plt.close()
print(rating_summary)

#plot rating vs iced level
rating_iced_summary = df.groupby(['Rating', 'Iced Level']).size().reset_index(name='Count')
rating_iced_pivot = rating_iced_summary.pivot(index='Rating', columns='Iced Level', values='Count').fillna(0)
rating_iced_pivot.plot(kind='bar', stacked=True)
plt.title('Rating vs Iced Level')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.legend(title='Iced Level')
plt.tight_layout()
plt.savefig('nlp/reviews/results/rating_vs_iced_level.png')
plt.close() 

print(rating_iced_summary)

sorted_pwp.to_csv('nlp/reviews/results/products_with_positive_iced_reviews.csv', index=False)