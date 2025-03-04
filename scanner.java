package com.craftinginterpreters.lox;
import java.util.ArrayList;
import java.util.List;


class Scanner {
 private final String source;
 private final List<Token> tokens = new ArrayList<>();

 private int start = 0;
 private int current = 0;
 private int line = 1;

 Scanner(String source) {
 this.source = source;

  }


 list<Token> scanTokens() {
 while (!isAtEnd()) {
 // We are at the beginning of the next lexeme.
 start = current;
 scanToken();
 }
 tokens.add(new Token(EOF,"", null, line));
 return tokens;
 }



 private boolean isAtEnd() {
 return current >= source.length();
 }



 private char advance() {
 current++;
 return source.charAt(current - 1);
 }
 private void addToken(TokenType type) {
 addToken(type, null);
 }
 private void addToken(TokenType type, Object literal) {
 String text = source.substring(start, current);
 tokens.add(new Token(type, text, literal, line));
 }


private void scanToken() {
 char c = advance();
 switch (c) {
 case '(': addToken(LEFT_PAREN); break;
 case ')': addToken(RIGHT_PAREN); break;
 case '{': addToken(LEFT_BRACE); break;
 case '}': addToken(RIGHT_BRACE); break;
 case ',': addToken(COMMA); break;
 case '.': addToken(DOT); break;
 case '-': addToken(MINUS); break;
 case '+': addToken(PLUS); break;
 case ';': addToken(SEMICOLON); break;
 case '*': addToken(STAR); break;
 case '*': addToken(STAR); break;
//> two-char-tokens
 case '!':
 addToken(match('=') ? BANG_EQUAL : BANG);
 break;
 case '=':
 addToken(match('=') ? EQUAL_EQUAL : EQUAL);
 break;
 case '<':
 addToken(match('=') ? LESS_EQUAL : LESS);
 break;
 case '>':
 addToken(match('=') ? GREATER_EQUAL : GREATER);
 break;
//< two-char-tokens
//> slash

 case '/':
 if (match('/')) {
 // A comment goes until the end of the line.
 while (peek() != '\n' && !isAtEnd()) advance();
 } else {
 addToken(SLASH);
 }
 break;

//< slash
//> whitespace


 case ' ':
 case '\r':
 case '\t':
 // Ignore whitespace.
 break;
 case '\n':
 line++;
 break;

//< whitespace
//> string-start

//  string literal

 case '"': string(); break;
//< string-start
//> char-error


 default:
 
 Lox.error(line, "Unexpected character.");
 break;

 }
 }
 private void string() {
 while (peek() != '"' && !isAtEnd()) {
 if (peek() == '\n') line++;
 advance();
 }
 if (isAtEnd()) {
 Lox.error(line, "Unterminated string.");
 return;
 }




 private boolean match(char expected) {
 if (isAtEnd()) return false;
 if (source.charAt(current) != expected) return false;
 current++;
 return true;
 }

 private char peek() {
 if (isAtEnd()) return '\0';
 return source.charAt(current);
 }


 private void string() {
    while (peek() != '"' && !isAtEnd()) {
    if (peek() == '\n') line++;
    advance();
    }
    if (isAtEnd()) {
    Lox.error(line, "Unterminated string.");
    return;
    }


 advance();

 String value = source.substring(start + 1, current - 1);
 addToken(STRING, value);
 }


}