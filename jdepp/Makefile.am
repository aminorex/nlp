SUBDIRS = src tools
EXTRA_DIST = GPL LGPL swig

model_topdir = model
classifier = @CLASSIFIER@
corpus = @CORPUS@
modeldir = ${model_topdir}/${corpus}
CLEANFILES = ${modeldir}/*
JDEPP = src/jdepp$(EXEEXT)
KYOTO_URL = http://nlp.ist.i.kyoto-u.ac.jp/DLcounter/lime.cgi?down=http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/corpus/KyotoCorpus4.0.tar.gz&name=KyotoCorpus4.0.tar.gz # respect counter CGI
KNBC_URL  = http://nlp.ist.i.kyoto-u.ac.jp/kuntt/KNBC_v1.0_090925.tar.bz2
UNIVERSAL_URL  = https://uni-dep-tb.googlecode.com/svn/trunk/universal_treebanks_v2.0.tar.gz

install-data-hook:
	@echo "Installing ${corpus} model.."
	if test -e ${modeldir}/dic.euc; then \
		$(INSTALL) -d $(DESTDIR)$(pkglibdir)/${modeldir}; \
		$(INSTALL) -p ${modeldir}/* $(DESTDIR)$(pkglibdir)/${modeldir}; \
	echo 'done.'; \
	fi
	@if ! test -e ${modeldir}/dic.euc; then \
		echo 'WARNING: No model has been built; try make model.'; \
	fi

dist-hook:
	cp $(srcdir)/tools/*.py $(distdir)/tools

uninstall-local:
	if test -e $(DESTDIR)$(pkglibdir)/${modeldir}; then \
		$(RM) $(DESTDIR)$(pkglibdir)/${modeldir}/*; \
	fi

kyoto-benchmark:
	$(MKDIR_P) ${model_topdir}/kyoto
	$(RM) ${model_topdir}/kyoto/*
	@test -e "$(KYOTO_CORPUS_DIR)" || (echo 'Kyoto University Text Corpus not found (KYOTO_CORPUS_DIR=$(KYOTO_CORPUS_DIR))' && exit 1)
	@echo "Converting corpus into JDP format.."
	cat $(KYOTO_CORPUS_DIR)/dat/syn/95{01{01,03,04,05,06,07,08,09,10,11},{01,02,03,04,05,06,07,08}ED}.KNP | @KYOTO_CONV@ > ${model_topdir}/kyoto/train.JDP.euc
	cat $(KYOTO_CORPUS_DIR)/dat/syn/95{01{12,13},09ED}.KNP | @KYOTO_CONV@ > ${model_topdir}/kyoto/dev.JDP.euc
	cat $(KYOTO_CORPUS_DIR)/dat/syn/95{01{14,15,16,17},{10,11,12}ED}.KNP | @KYOTO_CONV@ > ${model_topdir}/kyoto/test.JDP.euc
	@echo "done.\n"

kyoto:
	$(MKDIR_P) ${model_topdir}/kyoto
	$(RM) ${model_topdir}/kyoto/*
	@test -e "$(KYOTO_CORPUS_DIR)" || (echo 'Kyoto University Text Corpus not found (KYOTO_CORPUS_DIR=$(KYOTO_CORPUS_DIR))' && exit 1)
	@echo "Converting corpus into JDP format.."
	cat $(KYOTO_CORPUS_DIR)/dat/syn/*.KNP | @KYOTO_CONV@ > ${model_topdir}/kyoto/train.JDP.euc
	@echo "done.\n"

kyoto-tarball:
	@if ! test -e "$(KYOTO_CORPUS_DIR)"; then \
		echo "Kyoto University Text Corpus not found (KYOTO_CORPUS_DIR=$(KYOTO_CORPUS_DIR))"; \
		echo "Downloading Kyoto University Text Corpus.."; \
		if test $(CURL) != "no"; then \
			$(CURL) -o KyotoCorpus4.0.tar.gz -L $(KYOTO_URL) ; \
		elif test $(WGET) != "no"; then \
			$(WGET) -O KyotoCorpus4.0.tar.gz $(KYOTO_URL) ; \
		else \
			echo "no downloaders (curl, wget); I can't do anything more"; \
			exit 1; \
		fi; \
		wait ; \
		echo "done."; \
		echo "Extracting tarball.."; \
		tar zxf KyotoCorpus4.0.tar.gz; \
		echo "done."; \
	fi

kyoto-partial-benchmark: kyoto-tarball
	$(MKDIR_P) ${model_topdir}/kyoto-partial
	$(RM) ${model_topdir}/kyoto-partial/*
	@test -e "$(KYOTO_CORPUS_DIR)" || (echo 'Kyoto University Text Corpus not found (KYOTO_CORPUS_DIR=$(KYOTO_CORPUS_DIR))' && exit 1)
	@echo "Converting corpus into JDP format.."
	cat $(KYOTO_CORPUS_DIR)/dat/num/95{01{01,03,04,05,06,07,08,09,10,11},{01,02,03,04,05,06,07,08}ED}.num | grep -v "^+" | @KYOTO_CONV@ > ${model_topdir}/kyoto-partial/train.JDP.euc
	cat $(KYOTO_CORPUS_DIR)/dat/num/95{01{12,13},09ED}.num | grep -v "^+" | @KYOTO_CONV@ > ${model_topdir}/kyoto-partial/dev.JDP.euc
	cat $(KYOTO_CORPUS_DIR)/dat/num/95{01{14,15,16,17},{10,11,12}ED}.num | grep -v "^+" | @KYOTO_CONV@ > ${model_topdir}/kyoto-partial/test.JDP.euc
	@echo "done.\n"

kyoto-partial: kyoto-tarball
	$(MKDIR_P) ${model_topdir}/kyoto-partial
	$(RM) ${model_topdir}/kyoto-partial/*
	@test -e "$(KYOTO_CORPUS_DIR)" || (echo 'Kyoto University Text Corpus not found (KYOTO_CORPUS_DIR=$(KYOTO_CORPUS_DIR))' && exit 1)
	@echo "Converting corpus into JDP format.."
	cat $(KYOTO_CORPUS_DIR)/dat/num/*.num | grep -v "^+" | @KYOTO_CONV@ > ${model_topdir}/kyoto-partial/train.JDP.euc
	@echo "done.\n"

universal-tarball:
	@if ! test -e "$(UNIVERSAL_CORPUS_DIR)"; then \
		echo "Universal Dependency Treebank not found (UNIVERSAL_CORPUS_DIR=$(UNIVERSAL_CORPUS_DIR))"; \
		echo "Downloading Universal Dependency Treebank.."; \
		if test $(CURL) != "no"; then \
			$(CURL) -o universal_treebanks_v2.0.tar.gz -L $(UNIVERSAL_URL) ; \
		elif test $(WGET) != "no"; then \
			$(WGET) -O universal_treebanks_v2.0.tar.gz $(UNIVERSAL_URL) ; \
		else \
			echo "no downloaders (curl, wget); I can't do anything more"; \
			exit 1; \
		fi; \
		wait ; \
		echo "done."; \
		echo "Extracting tarball.."; \
		tar zxf universal_treebanks_v2.0.tar.gz; \
		echo "done."; \
	fi

universal-benchmark: universal-tarball
	$(MKDIR_P) ${model_topdir}/universal
	$(RM) ${model_topdir}/universal/*
	@test -e "$(UNIVERSAL_CORPUS_DIR)" || (echo 'Universal Dependency Treebank not found (UNIVERSAL_CORPUS_DIR=$(UNIVERSAL_CORPUS_DIR))' && exit 1)
	@echo "Converting corpus into JDP format.."
	cat $(UNIVERSAL_CORPUS_DIR)/std/ja/ja-universal-train.conll | @UNIVERSAL_CONV@ > ${model_topdir}/universal/train.JDP.euc
	cat $(UNIVERSAL_CORPUS_DIR)/std/ja/ja-universal-dev.conll | @UNIVERSAL_CONV@ > ${model_topdir}/universal/dev.JDP.euc
	cat $(UNIVERSAL_CORPUS_DIR)/std/ja/ja-universal-test.conll | @UNIVERSAL_CONV@ > ${model_topdir}/universal/test.JDP.euc
	@echo "done.\n"

universal: universal-tarball
	$(MKDIR_P) ${model_topdir}/universal
	$(RM) ${model_topdir}/universal/*
	@test -e "$(UNIVERSAL_CORPUS_DIR)" || (echo 'Universal Dependency Treebank not found (UNIVERSAL_CORPUS_DIR=$(UNIVERSAL_CORPUS_DIR))' && exit 1)
	@echo "Converting corpus into JDP format.."
	cat $(UNIVERSAL_CORPUS_DIR)/std/ja/ja-universal-*.conll | @UNIVERSAL_CONV@ > ${model_topdir}/universal/train.JDP.euc
	@echo "done.\n"

knbc-tarball:
	@if ! test -e "$(KNBC_CORPUS_DIR)"; then \
		echo "Kyoto-University and NTT Blog (KNB) Corpus not found: $(KNBC_CORPUS_DIR)"; \
		echo "Downloading KNB Corpus.."; \
		if test $(CURL) != "no"; then \
			$(CURL) -O $(KNBC_URL); \
		elif test $(WGET) != "no"; then \
			$(WGET) $(KNBC_URL); \
		else \
			echo "no downloaders (curl, wget); I can't do anything more"; \
			exit 1; \
		fi; \
		wait ; \
		echo "done."; \
		echo "Extracting tarball.."; \
		tar jxf KNBC_v1.0_090925.tar.bz2; \
		echo "done."; \
	fi

knbc-benchmark: knbc-tarball
	$(MKDIR_P) ${model_topdir}/knbc
	$(RM) ${model_topdir}/knbc/*
	find $(KNBC_CORPUS_DIR)/corpus1 -type f -name "KN*" | LC_ALL=C sort | $(AWK) -F'N|_' '$$(NF-2) % 6 <  4 { print }' | xargs cat | @KNBC_CONV@ > ${model_topdir}/knbc/train.JDP.euc
	find $(KNBC_CORPUS_DIR)/corpus1 -type f -name "KN*" | LC_ALL=C sort | $(AWK) -F'N|_' '$$(NF-2) % 6 == 4 { print }' | xargs cat | @KNBC_CONV@ > ${model_topdir}/knbc/dev.JDP.euc
	find $(KNBC_CORPUS_DIR)/corpus1 -type f -name "KN*" | LC_ALL=C sort | $(AWK) -F'N|_' '$$(NF-2) % 6 == 5 { print }' | xargs cat | @KNBC_CONV@ > ${model_topdir}/knbc/test.JDP.euc
	@echo "Converting corpus into JDP format.."

knbc: knbc-tarball
	$(MKDIR_P) ${model_topdir}/knbc
	$(RM) ${model_topdir}/knbc/*
	find $(KNBC_CORPUS_DIR)/corpus1 -type f -name "KN*" | LC_ALL=C sort | xargs cat | @KNBC_CONV@ > ${model_topdir}/knbc/train.JDP.euc
	@echo "Converting corpus into JDP format.."

kyoto+knbc-benchmark: kyoto-benchmark knbc-benchmark
	$(MKDIR_P) ${model_topdir}/kyoto+knbc
	$(RM) ${model_topdir}/kyoto+knbc/*
	cat ${model_topdir}/kyoto/train.JDP.euc ${model_topdir}/knbc/train.JDP.euc > ${model_topdir}/kyoto+knbc/train.JDP.euc
	cat ${model_topdir}/kyoto/dev.JDP.euc ${model_topdir}/knbc/dev.JDP.euc > ${model_topdir}/kyoto+knbc/dev.JDP.euc
	cat ${model_topdir}/kyoto/test.JDP.euc ${model_topdir}/knbc/test.JDP.euc > ${model_topdir}/kyoto+knbc/test.JDP.euc
	@echo "done.\n"

kyoto+knbc: kyoto knbc
	$(MKDIR_P) ${model_topdir}/kyoto+knbc
	$(RM) ${model_topdir}/kyoto+knbc/*
	cat ${model_topdir}/kyoto/train.JDP.euc ${model_topdir}/knbc/train.JDP.euc > ${model_topdir}/kyoto+knbc/train.JDP.euc

${modeldir}/dic.euc: model

model-benchmark: all ${corpus}-benchmark
	@echo "translate corpus into UTF-8.."
	for i in train dev test; do \
	  $(ICONV) -f EUC-JP -t UTF-8 ${modeldir}/$$i.JDP.euc > ${modeldir}/$$i.JDP.utf8; \
	done
	@echo "done."
	@echo "Training and testing BUNSETSU CHUNKER.."
	${JDEPP} -t 0 -I 1 -c ${modeldir}/train.JDP.utf8 -m ${modeldir} -- ${CHUNKER_LEARNER_OPT}
	@if test ${classifier} == "2ndPolyFST"; then \
	  ${JDEPP} -t 3 -I 1 -c ${modeldir}/train.JDP.utf8 -m ${modeldir} -- ${CHUNKER_LEARNER_OPT} -- ${CHUNKER_CLASSIFIER_OPT} -t 1; \
	fi
	${JDEPP} -t 1 -I 1 -c ${modeldir}/train.JDP.utf8 -m ${modeldir} -- ${CHUNKER_LEARNER_OPT} -- ${CHUNKER_CLASSIFIER_OPT} < ${modeldir}/test.JDP.utf8
	@echo "done."
	@echo "Training and testing DEPENDENCY PARSER.."
	${JDEPP} -t 0 -I 2 -c ${modeldir}/train.JDP.utf8 -m ${modeldir} -- ${PARSER_LEARNER_OPT}
	@if test ${classifier} == "2ndPolyFST"; then \
	  ${JDEPP} -t 3 -I 2 -c ${modeldir}/train.JDP.utf8 -m ${modeldir} -- ${PARSER_LEARNER_OPT} -- -- ${PARSER_CLASSIFIER_OPT} -t 1; \
	fi
	${JDEPP} -t 1 -I 2 -c ${modeldir}/train.JDP.utf8 -m ${modeldir} -- ${PARSER_LEARNER_OPT} -- -- ${PARSER_CLASSIFIER_OPT} < ${modeldir}/test.JDP.utf8
	@echo "done."
	@echo "Generating feature strings in EUC-JP"
	${JDEPP} -t 1 -e 1 -I 1 -c ${modeldir}/train.JDP.euc -m ${modeldir} < ${modeldir}/test.JDP.euc 2> /dev/null
	@echo "done."

model: all ${corpus}
	@echo "translate corpus into UTF-8.."
	$(ICONV) -f EUC-JP -t UTF-8 ${modeldir}/train.JDP.euc > ${modeldir}/train.JDP.utf8
	@echo "done."
	@echo "Training BUNSETSU CHUNKER.."
	${JDEPP} -t 0 -I 1 -c ${modeldir}/train.JDP.utf8 -m ${modeldir} -- ${CHUNKER_LEARNER_OPT}
	@if test ${classifier} == "2ndPolyFST"; then \
	  ${JDEPP} -t 3 -I 1 -c ${modeldir}/train.JDP.utf8 -m ${modeldir} -- ${CHUNKER_LEARNER_OPT} -- ${CHUNKER_CLASSIFIER_OPT} -t 1; \
	fi
	echo '' | ${JDEPP} -t 1 -I 1 -c ${modeldir}/train.JDP.utf8 -m ${modeldir} -- ${CHUNKER_LEARNER_OPT} -- ${CHUNKER_CLASSIFIER_OPT}
	@echo "done."
	@echo "Training and testing DEPENDENCY PARSER.."
	${JDEPP} -t 0 -I 2 -c ${modeldir}/train.JDP.utf8 -m ${modeldir} -- ${PARSER_LEARNER_OPT}
	@if test ${classifier} == "2ndPolyFST"; then \
	  ${JDEPP} -t 3 -I 2 -c ${modeldir}/train.JDP.utf8 -m ${modeldir} -- ${PARSER_LEARNER_OPT} -- -- ${PARSER_CLASSIFIER_OPT} -t 1; \
	fi
	echo '' | ${JDEPP} -t 1 -I 2 -c ${modeldir}/train.JDP.utf8 -m ${modeldir} -- ${PARSER_LEARNER_OPT} -- -- ${PARSER_CLASSIFIER_OPT}
	@echo "done."
	@echo "Generating feature strings in EUC-JP"
	@echo '' | ${JDEPP} -t 1 -e 1 -I 1 -c ${modeldir}/train.JDP.euc -m ${modeldir} 2> /dev/null
	@echo "done."

.PHONY: model knbc kyoto kyoto-partial kyoto+knbc
