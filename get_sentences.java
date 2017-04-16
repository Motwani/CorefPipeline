import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
import java.io.*;

import edu.stanford.nlp.process.*;
import edu.stanford.nlp.ling.*;
import org.apache.commons.io.*;
import org.apache.commons.lang3.*;
import edu.stanford.nlp.process.PTBTokenizer;
import edu.stanford.nlp.process.CoreLabelTokenFactory;
import edu.stanford.nlp.process.WordToSentenceProcessor;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.ling.HasWord;
// import edu.stanford.nlp.ling.Sentence;

public class get_sentences{
  public static void main(String [] args) throws FileNotFoundException,IOException
  {

    // System.out.println("HERE");
    FileInputStream inputStream = new FileInputStream("Resolved_The_Adv_Blue_Carbuncle.txt");
    // String paragraph = "My 1st sentence. “Does it work for questions?” My third sentence.";
    String paragraph = IOUtils.toString(inputStream);
    List<String> sentenceList;

    /* ** APPROACH 1 (BAD!) ** */
    // Reader reader = new StringReader(paragraph);
    // DocumentPreprocessor dp = new DocumentPreprocessor(reader);
    // sentenceList = new ArrayList<String>();
    // for (List<HasWord> sentence : dp) {
    //     sentenceList.add(Sentence.listToString(sentence));
    // }
    // System.out.println(StringUtils.join(sentenceList, " _ "));

    /* ** APPROACH 2 ** */
    //// Tokenize
    List<CoreLabel> tokens = new ArrayList<CoreLabel>();
    PTBTokenizer<CoreLabel> tokenizer = new PTBTokenizer<CoreLabel>(new StringReader(paragraph), new CoreLabelTokenFactory(), "");
    while (tokenizer.hasNext()) {
      tokens.add(tokenizer.next());
    }
    //// Split sentences from tokens
    List<List<CoreLabel>> sentences = new WordToSentenceProcessor<CoreLabel>().process(tokens);
    //// Join back together
    int end;
    int start = 0;
    sentenceList = new ArrayList<String>();
    for (List<CoreLabel> sentence: sentences) {
      end = sentence.get(sentence.size()-1).endPosition();
      sentenceList.add(paragraph.substring(start, end).trim());
      start = end;
    }
    System.out.println(StringUtils.join(sentenceList, "\n"));
    // System.out.println(Arrays.toString(sentenceList.toArray()));
  }
}
