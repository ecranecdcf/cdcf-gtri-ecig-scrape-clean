import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

label_format = '''<View>
  <Text name="text" value="$Review"/>
  <View style="box-shadow: 2px 2px 5px #999;                padding: 20px; margin-top: 2em;                border-radius: 5px;">
    <Header value="Does the review indicate the product is iced?"/>
    <Choices name="iced" toName="text" choice="single" showInLine="true">
      <Choice value="true"/>
      <Choice value="false"/>
    </Choices>
  </View>
</View><!-- {
  "data": {"text": "This is a great 3D movie that delivers everything almost right in your face."}
} -->'''


file_name = 'nlp/reviews/results/prompt_v4_500_labels.csv'

df = pd.read_csv(file_name)

truth_label = 'iced'
predicted_label = 'Review Indicated Iced'

filtered_df = df[df[truth_label].notna()]
cols = filtered_df[[predicted_label, truth_label]]

precision = precision_score(filtered_df[truth_label], filtered_df[predicted_label])
recall = recall_score(filtered_df[truth_label], filtered_df[predicted_label])
f1 = f1_score(filtered_df[truth_label], filtered_df[predicted_label])
accuracy = accuracy_score(filtered_df[truth_label], filtered_df[predicted_label])


print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")
print(f"Accuracy: {accuracy:.2f}")

print(filtered_df.shape)


### Version 2, based on 545
# model: "hosted_vllm/openai/gpt-oss-20b"
# Precision: 0.88
# Recall: 0.73
# F1 Score: 0.80
# Accuracy: 0.96

### Version 3, based on 524
# Precision: 0.61
# Recall: 0.72
# F1 Score: 0.66
# Accuracy: 0.94

### Version 4, based on 507
# Precision: 0.94
# Recall: 0.79
# F1 Score: 0.86
# Accuracy: 0.98