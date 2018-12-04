int main() {
	int a;

	a = 10;

	if(a > 0)
		a = 0;

	print("INICIO DO WHILE");
	while(a >= 0) {
		print(a);
		a = a - 1;
	}

	return 0;
}