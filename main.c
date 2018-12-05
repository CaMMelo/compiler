/*==============================
**  Programa exemplo em miniC
**
**  - fatora um inteiro lido.
**==============================*/

int main() {
	int n;
	n = 20;

	for(;n>=0;) {
		print(n, ", ");
		if(n == 3)
			continue;
		n = n - 1;
	}

	while(1) {
		print("SE FUDEU!");
	}

	return 0;
}