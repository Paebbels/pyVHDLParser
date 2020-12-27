from unittest import TextTestRunner, TestLoader


def suite():
	# suite = TestSuite()
	# suite.addTests(Tokens.Sequence_1())
	# suite.addTests(Tokens.Sequence_2())

	tl = TestLoader()
	suite = tl.loadTestsFromModule(tests.unit.Tokenizer.Tokens)

	return suite

if __name__ == '__main__':
	runner = TextTestRunner()
	runner.run(suite())
