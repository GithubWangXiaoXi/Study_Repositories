### IDEA导入Eclipse项目报错`Tomcat Exception: java.lang.reflect.InvocationTargetException, java.lang.SecurityException, org.xml.sax.SAXNotRecognizedException`怎么办

修改tomcat的配置文件，末尾加入如下配置即可

```
javax.xml.parsers.DocumentBuilderFactory=com.sun.org.apache.xerces.internal.jaxp.DocumentBuilderFactoryImpl
javax.xml.transform.TransformerFactory=com.sun.org.apache.xalan.internal.xsltc.trax.TransformerFactoryImpl
javax.xml.parsers.SAXParserFactory=com.sun.org.apache.xerces.internal.jaxp.SAXParserFactoryImpl
javax.xml.datatype.DatatypeFactory=com.sun.org.apache.xerces.internal.jaxp.datatype.DatatypeFactoryImpl
```

参考[Tomcat Exception: java.lang.reflect.InvocationTargetException, java.lang.SecurityException, org.xml.sax.SAXNotRecognizedException](https://stackoverflow.com/questions/58484733/tomcat-exception-java-lang-reflect-invocationtargetexception-java-lang-securit)