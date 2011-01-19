# Mom, Dad, if you're reading this, I'm very sorry.

include configs/linux-llvm.llvmcore

llvmcore:
	gcc -fPIC -shared -o libllvmcore-$(shell llvm-config --version).so -Wl,--whole-archive $(shell llvm-config --ldflags) $(LLVM_LIBS) -Wl,--no-whole-archive
