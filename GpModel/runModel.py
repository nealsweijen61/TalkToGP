from data.customClassifier import CustomClassifier

expr = "((((x1+x9)+41.432000)/ ((x10/ (x2+1e-6) )+1e-6) )+(x8+x8))"
classifier = CustomClassifier(expr)
X = [[3,0,7,0,6,0,1,0.686667,0.638263,0.585,0.208342]]
res = classifier.predict(X)
print(res)