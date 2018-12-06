/*==============================
**  Programa exemplo em miniC
**
**  - fatora um inteiro lido.
**==============================*/

int main() {
	int n;
	n = 20;
    
    scan("digite o valor de n: ", n);
    
	for(;n>=0;) {
		print(n, "\n");
		n = n - 1;
	}

	if(n < 20) {
		n = 10;
	}

	print("TOMA SEU N: ", n, "\n");

	return 0;
}
