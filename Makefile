indexgen:
	clear
	rm index.txt
	python index_gen.py
	subl index.txt

indexgen3x3:
	rm index_3x3.txt
	python index_gen.py
	subl index_3x3.txt

convolution:
	python full_conv.py

# ============== MAKES DE TESTE PYTHON ============== 
		
test_w:
	clear
	python w_test.py

wtest_xi:
	clear
	python wtest_xi.py]

cqint8:
	clear
	python CQint8_test.py