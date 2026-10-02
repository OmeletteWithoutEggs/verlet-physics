import vectors

n = vectors.Vector2(10,10)
v = vectors.Vector2(20,20)
t = vectors.dot(n,v)
print((v.magnitude()/n.magnitude())*t)