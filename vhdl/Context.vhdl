context ctx1 is
	use lib1.pkg1.all;
end context;

context ctx2 is
	library lib21, lib22;
	use lib21.pkg21.all;
	use lib22.pkg22.all;
end context;

context ctx3 is use lib3.pkg3.all; end context ctx3;

context
	ctx4
		is
			use lib4.pkg4.all;
				end
					context
						;
