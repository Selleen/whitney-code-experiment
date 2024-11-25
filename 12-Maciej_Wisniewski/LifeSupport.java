import java.io.*;
import java.util.*;import java.text.*;
import java.time.LocalTime;
import javax.servlet.*;import javax.servlet.http.*;public
class LifeSupport extends HttpServlet {public void doGet(HttpServletRequest
question, HttpServletResponse answer)throws ServletException, IOException {
  String title ="The Meaning of Life as Expressed in Seven Lines of Code by Maciej Wisniewski";
  answer.setContentType("text/html");
PrintWriter out=answer.getWriter();
LocalTime now = LocalTime.now();
int currentHour = now.getHour();
                                           int colors = 0;String[] dates = new String[24];
                                             String[] stories = new String[6];for(int i=0;
                   i<dates.length;i++){GregorianCalendar calendar=
               new GregorianCalendar((int)(Math.random()*102)+1900,
                (int)(Math.random()*12), (int)(Math.random()*30));
                                                Date date = calendar.getTime();DateFormat dateFormat
                  = DateFormat.getDateInstance(DateFormat.LONG);String
                dateOfEvent = dateFormat.format(date);dates[i] =
                dateOfEvent;}String[] zone_1 = {"in New YorkCity...",
                "in Havana...", "in Ottawa...", "in Montreal...",
             "in Philadelphia...", "in Asuncion...",
           "in Atlanta...", "in San Juan...",
            "in Santiago...", "in Santo Domingo...",
          "in Boston...", "in La Paz...",
         "in Caracas...","in Toronto...",
       "in Detroit...","in Washington DC...",
       "in Harrisburg...", "in Iqaluit...",
       "in Kingstown...","in Nassau..."};
       String[] zone_2 = {"in Buenos Aires...",
       "in Brasilia...", "in Sao Paulo...",
       "in Rio de Janeiro...", "in Casablanca...",
       "in Reykjavik...", "in Algiers...",
       "in Lagos...","in Lisbon...",
       "in London...","in Dublin...",
       "in Odessa...","in Harare...",
       "in Prague...","in Stockholm...",
       "in Warsaw...","in Kuwait City...",
       "in Nairobi...", "in Istanbul...",
       "in Moscow..."};String[] zone_3 =
       {"in Bangkok...","in Jakarta...",
       "in Hanoi...", "in Bandung...",
       "in Astana...", "in Almaty...",
       "in Phnom Penh...","in Saigon...",
       "in Semarang...", "in Surabaya...",
       "in Surakarta...", "in Malang...",
       "in Medan...","in The Settlement...",
       "in Mexicali...","in Tijuana...",
       "in Vientiane...","in Novosibirsk...",
       "in Omsk...","in Palembang..."};
       String[] zone_4 ={"in Manila...",
       "in Taipei...","in Singapore...",
       "in Shanghai...","in Kuala Lumpur...",
       "in Beijing...","in Perth...",
       "in Hong Kong...","in Chongquing...",
       "in Mataram...","in Tangshan...",
       "in Tientsin...","in Denpasar...",
       "in Tsingtao...","in Endeh...",
       "in Hangzhou...","in Seoul...",
       "in Tokyo...","in Ulaanbaatar...",
       "in Nagoya..."};String[] zone_5 =
       {"in Brisbane...", "in Sydney...",
       "in Canberra...", "in Melbourne...",
       "in Vladivostok...", "in Suva...",
       "in Noumea...", "in Honiara...",
       "in Kolonia...", "in Wellington...",
       "in Kamchatka...", "in Anadyr...",
       "in Honolulu...", "in Kiritimati...",
       "in Anchorage...", "in Phoenix...",
       "in San Francisco...", "in Seattle...",
       "in Los Angeles...", "in Vancouver..."};
                                    String[] zone_6 = {"in Aklavik...",
       "in San Salvador...", "in Managua...",
       "in Tegucigalpa...", "in Denver...",
       "in Edmonton...", "in Guatemala...",
       "in Houston...", "in Indianapolis...",
       "in Kingston...", "in Bogota...",
       "in St. Paul...", "in Lima...",
       "in Mexico City...", "in Chicago...",
       "in Minneapolis...", "in Montgomery...",
       "in Winnipeg...", "in New Orleans...",
       "in Acapulco..."};int[] zoneColors=new
        int[6];if (currentHour==7){colors = 180;
        zoneColors[0]= 180;zoneColors[1]= 240;
        zoneColors[2]= 180; zoneColors[3]= 120;
        zoneColors[4]= 60;zoneColors[5]= 120;
                                stories[0] = "On the morning of ";
                                stories[1] = "During the day of ";
                                stories[2] = "In the early evening on ";
                                stories[3] = "On the evening of ";
                                stories[4] = "During the night of ";
                                stories[5] = "In the early morning on ";}
                                else if (currentHour==18){colors = 180;
        zoneColors[0] = 180;zoneColors[1] = 120;
                                zoneColors[2] = 60;zoneColors[3] = 120;
                                zoneColors[4] = 180;zoneColors[5] = 240;
                                stories[0] = "In the early evening on ";
                                stories[1] = "On the evening of ";
                                stories[2] = "During the night of ";
                                stories[3] = "In the early morning on ";
                                stories[4] = "On the morning of ";
                                stories[5] = "During the day of ";}
                                else if(currentHour==5||currentHour==6){
                                colors = 120;zoneColors[0] = 120;
                                zoneColors[1]=180;zoneColors[2]=240;
                                zoneColors[3]=180;zoneColors[4]=120;
                                zoneColors[5]=60;//zoneColors[0]=60;
                                stories[0] = "In the early morning on ";
                                stories[1] = "On the morning of ";
                                stories[2] = "During the day of ";
                                stories[3] = "In the early evening on ";
                               stories[4] = "On the evening of ";
                              stories[5] = "During the night of ";}
                             else if (currentHour==19||
                  currentHour==20){colors=120;
                          zoneColors[0] = 120;
                         zoneColors[1] = 60;
                        zoneColors[2] = 120;
                       zoneColors[3] = 180;
                      zoneColors[4]= 240;
                     zoneColors[5]
       =180;
stories[0]
= "On the evening of ";
stories[1] = "During the night of ";
stories[2] = "In the early morning on ";stories[3] =
"On the morning of ";stories[4] = "During the day of ";
stories[5] = "In the early evening on ";}else if (currentHour >=
8 && currentHour <= 17){colors = 240;zoneColors[0] = 240;zoneColors[1] = 180;
zoneColors[2] = 120; zoneColors[3] = 60;zoneColors[4] = 120;zoneColors[5] = 180;
stories[0] = "During the day of "; stories[1] = "In the early evening on ";stories[2] =
"On the evening of ";stories[3] = "During the night of ";stories[4] = "In the early morning on ";
stories[5] = "On the morning of ";}else{colors = 60;zoneColors[0]=60;zoneColors[1]=120;
zoneColors[2]=180;zoneColors[3] = 240;zoneColors[4] = 180;zoneColors[5] = 120;stories[0] =
"During the night of "; stories[1]="In the early morning on ";stories[2] = "On the morning of ";
stories[3] = "During the day of ";   stories[4] = "In the early evening on ";stories[5] ="On the evening of";}
out.println("<html><head><title>");out.println(title);out.println("</title></head><body>");
out.println("<center><table cellspacing=\"1\" cellpadding=\"1\" border=\"0\">");for (int i = 0; i < 4; i++)
{out.println("<tr>" + "<td><applet code=\"Couplet\" height=\"140\" width=\"140\"><param name="+
"\"the meaning of life is....\"value=\""+ zone_1[(int)(Math.random()*20)] +"\"><param name=\"but wait\""+
"value=\""+ zoneColors[0] +"\"><param name=\"the meaning of life is..\" value=\""+ dates[(int)(Math.random()*24)]
+"\"><param name=\"the meaning of life is...\""+"value=\""+stories[0]+"\"></applet></td>"+
"<td><applet code=\"Couplet\" height=\"140\" width=\"140\"><param name=\"the meaning of life is....\" value=\""
+ zone_2[(int)(Math.random()*20)] +"\"><param name=\"but wait\" value=\""+ zoneColors[1]+
"\"><param name=\"the meaning of life is..\" value=\""+ dates[(int)(Math.random()*24)] +
"\"><param name=\"the meaning of life is...\" value=\""+ stories[1] +"\"></applet></td>" +
"<td><applet code=\"Couplet\" height=\"140\" width=\"140\"><param name=\"the meaning of"+
"life is....\" value=\""+zone_3[( int ) (Math.random()*20)]   +"\"> <param name=\"but wait\""+
"value=\""+ zoneColors[2] +"\"><param  name=\"the meaning of life is..\"value=\""+
dates[(int)(Math.random()*24)] +"\"><param name=\"the meaning of life is...\"value=\""
+stories[2]+"\"></applet></td>"+"<td> <applet code=\"Couplet\"  height= \"140\" width="+
"\"140\"> <param  name="+"\"the meaning of life is....\"  value=\""+
zone_4[(int ) ( Math.random()*20)]+"\"><param name=\"but wait\" value=\""+
zoneColors[3] + "\"><param name="+"\"the meaning of life is..\""+
"value=\""+dates[(int)(Math.random()*24)]//bla, bla,bla
+"\"><param name=\"the meaning of life is...\" value=\""+ stories[3]
+"\"></applet></td>"+"<td><applet code=\"Couplet\" height=\"140\""+
"width=\"140\"><param name=\"the meaning of life is....\""+
"value=\""+ zone_5[(int)(Math.random()*20)] +
"\"><param name=\"but wait\" value=\""+
zoneColors[4] +"\"><param name="+ "\"the meaning of life is..\""
+"value=\""+ dates[(int)(Math.random()*24)]
+"\"><param name=\"the meaning of life is...\" value=\""+
stories[4] +"\"></applet></td>" +
         "<td><applet code=\"Couplet\""+
            " height=\"140\" width=\"140\">"
               + "<param name=\"the meaning of life is....\" value=\""
                 + zone_6[(int)(Math.random()*20)]
                  +"\"><param name=\"but wait\" value=\""
                    + zoneColors[5] +"\"><param name=\"the meaning of life is..\" value=\""
                       + dates[(int)(Math.random()*24)]
                         +"\"><param name="+"\"the meaning of life is...\" value=\""+
                          stories[5] +"\"></applet></td>"
                             +"</tr>");}
                               out.println("</table></center>");
                                 out.println("</BODY></HTML>");
                                      out.close();}}