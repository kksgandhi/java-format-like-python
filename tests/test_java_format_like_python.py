import os
from textwrap import dedent

from java_format_like_python import Formatter


def test_format1():
    correct_output = dedent(
        """
        public class test_file                                                          {

            public static void main(String[] args)                                      {
                // This is a comment

                for(int i = 0; i < 3; i++)                                              {
                    System.out.println("Hello World")                                   ;}

                if (true)                                                               {
                    if(false)                                                           {
                        System.out.println("Hello World")                               ;}

                    else                                                                ;

                        System.out.println("Hello World")                               ;}
    """
    ).strip()

    path = os.path.join(os.path.dirname(__file__), "test_file.java")
    lines = [line for line in open(path).readlines()]

    new_lines = Formatter().format(lines)

    actural_output = "\n".join(new_lines).rstrip()
    assert actural_output == correct_output


def test_format2():
    correct_output = dedent(
        """
        public class other_test_file                                                    {
            public static void main(String[] args)                                      {
                //Calculates the sum of numbers 1 to 10
                int sum = 0                                                             ;
                boolean addFive = false                                                 ;

                for (int i = 1; i <= 10; i++)                                           {
                    sum += i                                                            ;}

                if (addFive)                                                            {
                    sum += 5                                                            ;
                    System.out.println(sum)                                             ;}

                else                                                                    {
                    System.out.println(sum)                                             ;}}}

    """
    ).strip()

    path = os.path.join(os.path.dirname(__file__), "other_test_file.java")
    lines = [line for line in open(path).readlines()]

    new_lines = Formatter().format(lines)

    actural_output = "\n".join(new_lines).rstrip()
    assert actural_output == correct_output
