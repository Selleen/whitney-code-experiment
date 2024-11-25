import java.awt.*; import java.applet.*; /*import good.luck.*/
/*
 * @title The Meaning of Life as Expressed in Seven Lines of Code
 * @author  Maciej Wisniewski
 * @version    The ultimate version
 */
/*
'The Meaning of Life as Expressed in Seven Lines of Code'
is a living clock/sundial of sort where time elapses, geography
stretches and history digresses.
The three connecting points are: destination, origin and its external
context.
The destination (as defined in Couplet.java) is a non-interactive
sundial that reflects changes in daylight. The origin (as defined in the
LifeSupport.java) computes time and history based on its geographical
location, and its own understanding of the Gregorian calender and
astronomy. It then links the results to the physical world.
The first two points are contained within the network's own topology. /v2/img/enterproject.gif
The third point is a metaphorical link to the external world.
While the program has no inherent understanding of celestial body
movements or physical laws, the code relocation to another geographical
site will properly reflect the amount of daylight as expressed through
the varying grays of the interface.
'The Meaning of Life as Expressed in Seven Lines of Code' depicts a
skewed view of geography, time and history, where space and time elapses
during the day and at night and stretches itself at sunrise and sunset.
*/
public class Couplet extends Applet



{public void paint(Graphics tellMe)// What is the meaning of life?

{int a_hint = Integer.parseInt(getParameter("but wait"));

setBackground (new Color (a_hint, a_hint, a_hint));



tellMe. drawString( getParameter ("the meaning of life is.."), 5, 65);

tellMe. drawString( getParameter ("the meaning of life is..."), 5, 35);

tellMe. drawString( getParameter ("the meaning of life is...."), 5, 95);}}


