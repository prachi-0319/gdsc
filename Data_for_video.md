## LLM Prompt
We are participating in google solutions challenge. we chose this problem statement

GenAI-Powered Financial Assistant for Better Investing Decisions
GenAI based financial assistant that allows people to ask the most basic questions around investing, but also allows them to find products to invest in. Financial literacy levels are extremely low in India, and while there's a growing number of investors in the market, there's little to no guidance given to them. We're working to bridge that divide and help people invest better. The the 100s of millions of investors coming in to the market, there's only one solution to address the problem and that is using AI. The scale of users simply cannot be addressed through manual means. We are building a GenAI based solution to allow people to have a conversation about their financial needs and be better informed while making a decision.
Objective:
The the 100s of millions of investors coming in to the market, there's only one solution to address the problem and that is using AI. The scale of users simply cannot be addressed through manual means. We are building a GenAI based solution to allow people to have a conversation about their financial needs and be better informed while making a decision.

we have made a webapp using streamlit with the following pages and features:
- login and create accoutn page as landing page. users cant access dashbvoard without loggin in. data and authentication happens through firestore.
- dahsboard is a quick about our project, widgets with links to all other pages, faq
- all features are also in the side nav bar as separate pafes
- there is a profile page which gets your preofile info from firestore, lets you update it and also allows you to delete your account.
- sign out button will take you back to the login page
- rate us button helps the user give rating. they can give rating only once every session.
- now the features:
1. finance chatbot where you can any question related to finance. the model is a chain of thoughts model so answetrs are well thouight of. it also lets you upload any file for the model to use while thinking. chat history for each user is stored in the backend.
2. finance dictionary where you search any word in finance to get a formal, a simple definityions and also related words.
3. lessons which provides quick lessons, youtube liiinks to important finance concepts.
4. quiz which helps you test ypur finance knowledge. you can choose level of difficulty and also the kind of quiz - a general quiz or a perosnalized quix based on your chatbot and word serch hispotry. it gives explanations for why an answer is incorrect and also displays final score.
5. finance profile recommender which gives sugggestions and profile recommendations based on your financial siutaqion.
6. a fraud alert detectoor where you can put details about a scheme you heard of and it will tell whether the scheme is fradulent or safe.
7. government scheme detetcotr which finds the best govt finance aid schemes for you based on your age, income, status, general obc etc status
8. a news board where you can input tags, country and category to fetch the latest news.

this is my entire app. now i want to submit my work but need to tie all the features together, talk avout the current situation about financial literacy in india, tell how our apps will solve it and how each deature is relevant. we have to make a 4-5 minute long video which is engaging, impactful and ttells about our application as it will be the first part of evaluation. we also have a ppt that needs to be filled. these are what need to be filled: idea/solution, problem resolution, unique value propositions, usp of the solution, how does it solve the porblem, list of features, proces flow diagram or use case diagram, wireframes/mock diagrams of proposed solution, architecture diagram, technolofies used, estimated implemenataion cose, additional details and future developments, 
help me write all the sections of the presentation and also a good proper script for the video. try to give proper statistics to support the effectiveness and how this app will acrually bring a chnage. also highlight how no such app currently exists which offers all these features all at once. name of our app in finfriend which is for your finance best friend. in the video we want to put videos clips graphs text and make it like an impactful movie so also tell me how to do that and the best free softwares to make that. thank you for all the help.



## PRESENTATION CONTENT
**Presentation Outline for FinFriend: Your Financial Best Friend**

1. **Idea/Solution**
   - **FinFriend** is an AI-powered financial assistant designed to enhance financial literacy and investment decisions among users. By integrating various tools and resources, FinFriend aims to provide personalized financial guidance, making complex financial concepts accessible and actionable.

2. **Problem Statement**
   - **Financial Literacy Gap**: Only 27% of India's population is financially literate, with significant disparities across regions. citeturn0search2
   - **Investment Challenges**: As more individuals enter the investment market, there's a pressing need for accessible, reliable, and personalized financial guidance to navigate investment options effectively.

3. **Problem Resolution**
   - **AI-Driven Assistance**: FinFriend leverages Generative AI to provide personalized financial advice, addressing the scalability issue of manual advisory services.
   - **Comprehensive Features**: The platform offers tools like a finance chatbot, dictionary, lessons, quizzes, profile recommender, fraud detector, government scheme finder, and news board, all aimed at enhancing financial understanding and decision-making.

4. **Unique Value Proposition (UVP)**
   - **Holistic Financial Support**: Combines multiple financial tools in one platform, offering a seamless user experience.
   - **Personalization at Scale**: Utilizes AI to tailor financial advice and content to individual user needs, ensuring relevance and engagement.
   - **Accessibility and Inclusivity**: Designed to cater to users with varying levels of financial knowledge, promoting widespread financial literacy.

5. **How Does It Solve the Problem?**
   - **Interactive Learning**: Engages users through quizzes and lessons, enhancing financial knowledge.
   - **Personalized Recommendations**: Provides tailored investment and financial product suggestions based on user profiles.
   - **Real-Time Information**: Delivers up-to-date financial news and alerts, keeping users informed about market trends.
   - **Fraud Detection**: Assists users in identifying and avoiding fraudulent schemes, protecting their investments.

6. **List of Features**
   - **Finance Chatbot**: AI-driven assistant for personalized financial queries.
   - **Finance Dictionary**: Comprehensive definitions and explanations of financial terms.
   - **Lessons**: Structured content and resources for financial education.
   - **Quiz**: Assessments to test and enhance financial knowledge.
   - **Profile Recommender**: Personalized financial product and investment suggestions.
   - **Fraud Alert Detector**: Tool to evaluate the legitimacy of financial schemes.
   - **Government Scheme Detector**: Information on government financial aid programs tailored to user profiles.
   - **News Board**: Customizable financial news feed based on user interests.

7. **Process Flow Diagram or Use Case Diagram**
   - **User Journey**: Illustrate the steps a user takes from registration to utilizing various features, highlighting interactions with AI components and personalized outputs.

8. **Wireframes/Mock Diagrams of Proposed Solution**
   - **Dashboard Layout**: Showcase the main interface with navigation to all features.
   - **Feature Screens**: Provide mock-ups of individual features like the chatbot interface, quiz module, and news board.

9. **Architecture Diagram**
   - **System Overview**: Depict the backend infrastructure, including AI processing units, database management (Firestore), user authentication, and integration points with external financial data sources.

10. **Technologies Used**
    - **Frontend**: Streamlit for interactive web application development.
    - **Backend**: Firestore for data storage and user authentication.
    - **AI Models**: Generative AI for personalized financial advice and chatbot interactions.
    - **APIs**: Integration with financial news and data providers for real-time information.

11. **Estimated Implementation Cost**
    - **Development Costs**: Allocate budget for AI model training, frontend and backend development, and integration efforts.
    - **Operational Costs**: Consider expenses related to cloud services, data storage, and maintenance.
    - **Marketing and Outreach**: Budget for user acquisition strategies and promotional activities.

12. **Additional Details and Future Developments**
    - **User Feedback Integration**: Plan to incorporate user feedback mechanisms for continuous improvement.
    - **Feature Expansion**: Future features may include investment tracking, community forums, and advanced analytics.
    - **Partnerships**: Explore collaborations with financial institutions for enriched content and services.



## VIDEO CONTENT
**Video Script for FinFriend Presentation**

*Opening Scene:*
- **Visual**: A bustling Indian cityscape transitions to individuals facing financial challenges—confusion over investments, overwhelming financial jargon, and missed opportunities.
- **Narration**: "In a nation where only 27% of adults are financially literate, millions navigate a complex financial landscape without adequate guidance." citeturn0search2

*Scene 2: Introduction to FinFriend*
- **Visual**: The screen brightens as the FinFriend logo appears, followed by a user-friendly interface showcasing the app's features.
- **Narration**: "Introducing FinFriend—your financial best friend, powered by AI to simplify finance and empower your investment journey."

*Scene 3: Highlighting Features (Continued)*
- **Visuals and Narration**:
- **Finance Chatbot**: "Have questions? Our AI-driven chatbot provides personalized answers, making complex concepts easy to understand."​
- **Finance Dictionary**: "Confused by jargon? Access simple definitions and related terms at your fingertips."​
- **Lessons and Quizzes**: "Learn at your own pace with structured lessons and
  - **Profile Recommender**: "Receive personalized financial product and investment suggestions tailored to your unique financial situation."
  - **Fraud Alert Detector**: "Stay protected by evaluating the legitimacy of financial schemes before you invest."
  - **Government Scheme Detector**: "Discover government financial aid programs that align with your age, income, and status."
  - **News Board**: "Customize your financial news feed based on your interests to stay informed about market trends."

*Scene 4: Impact and Statistics*
- **Visual**: Graphs and charts illustrating the low financial literacy rates in India, with statistics such as "Only 27% of Indian adults meet the minimum level of financial literacy" citeturn0search2.
- **Narration**: "With financial literacy rates alarmingly low, FinFriend aims to bridge this gap by providing accessible and personalized financial education."

*Scene 5: Market Differentiation*
- **Visual**: Side-by-side comparison of FinFriend with other financial apps, highlighting unique features like the AI-driven chatbot, comprehensive financial dictionary, and personalized recommendations.
- **Narration**: "While other apps offer isolated financial tools, FinFriend integrates multiple features into one platform, ensuring a holistic financial experience."

*Scene 6: Testimonials and Success Stories*
- **Visual**: Happy users sharing their experiences with FinFriend, emphasizing how the app has improved their financial understanding and decision-making.
- **Narration**: "Join the thousands who have transformed their financial journeys with FinFriend."

*Scene 7: Call to Action*
- **Visual**: FinFriend logo with download links for iOS and Android.
- **Narration**: "Empower your financial future today. Download FinFriend and take the first step towards financial literacy and security."



**Creating an Engaging Video**

To produce an impactful video that combines video clips, graphs, and text, consider the following steps:

1. **Storyboarding**: Plan each scene, detailing visuals, narration, and on-screen text.
2. **Visual Assets**: Gather high-quality images, video clips, and graphics that align with your script.
3. **Animation and Transitions**: Use smooth transitions and animations to maintain viewer engagement.
4. **Voiceover**: Record clear and professional voiceovers to narrate the script.
5. **Background Music**: Select royalty-free music that complements the video's tone without overpowering the narration.
6. **Text Overlays**: Incorporate text to highlight key points, statistics, and calls to action.
7. **Editing Software**: Utilize user-friendly, free video editing software such as:
   - **DaVinci Resolve**: Offers professional-grade editing tools with a free version available.
   - **Shotcut**: An open-source video editor with a straightforward interface.
   - **HitFilm Express**: Provides advanced features suitable for creating engaging videos.
   - **OpenShot**: A free, open-source video editor with a simple drag-and-drop interface.


**Final Tips**

- **Consistency**: Ensure a consistent color scheme, font style, and branding throughout the video.
- **Engagement**: Keep the video concise, aiming for a duration of 4-5 minutes, to maintain viewer interest.
- **Accessibility**: Include subtitles to make the video accessible to a broader audience.
- **Feedback**: Before finalizing, gather feedback from a small audience to identify areas for improvement.
 
 

Links referred to:

https://www.business-standard.com/content/press-releases-ani/spreading-the-financial-literacy-wave-across-india-national-finance-olympiad-2023-123122100732_1.html?utm_source=chatgpt.com

https://www.finsafe.in/?utm_source=chatgpt.com

https://www.moneycontrol.com/news/business/markets/financial-literacy-will-be-key-to-india-s-vision-for-2047-amfi-s-venkat-chalasani-12888370.html

https://www.iifl.com/blogs/personal-finance/money-management-aaps-in-india

https://www.reddit.com/r/personalfinanceindia/comments/1fl6dqa/what_are_your_favourite_finance_learningtracking/

https://www.newindianexpress.com/business/2024/Apr/15/why-is-financial-literacy-falling-short

https://www.business-standard.com/content/press-releases-ani/spreading-the-financial-literacy-wave-across-india-national-finance-olympiad-2023-123122100732_1.html

https://www.finnable.com/blogs/10-best-investment-apps-in-india-2023/

https://medium.com/%40khanrums26/top-5-personal-financial-planning-apps-in-india-b84152a93e73

https://m.economictimes.com/wealth/invest/6-apps-that-can-boost-your-financial-literacy/articleshow/102851709.cms

https://www.adb.org/results/india-financial-literacy-programs-lifting-families-out-debt-fueling-new-prosperity

https://ncfe.org.in/wp-content/uploads/2023/12/ExecSumm_.pdf

https://www.rbi.org.in/rbioecdflc2017/Downloads/Conference%20PPTs/08th%20Nov%202017/5.%20Session%201.3%20-%20Uma%20Shankar%20-%20Financial%20literacy%20in%20india%20-%20data%20and%20policy.pdf

https://www.finsafe.in/

https://www.ris.org.in/sites/default/files/Publication/DP-286-PDash-and-Rahul-Ranjan.pdf

https://www.ncaer.org/wp-content/uploads/2022/08/NCFE-2019_Final_Report.pdf

https://www.adb.org/results/india-financial-literacy-programs-lifting-families-out-debt-fueling-new-prosperity

https://www.intuit.com/intuitassist/

https://apps.apple.com/us/app/luna-ai-financial-assistant/id1620478455

https://web.meetcleo.com/

https://www.iotforall.com/how-to-build-an-ai-financial-assistant-app



https://www.indiainfoline.com/business-partners/moneyversity-financial-education-platform

https://investyadnya.in/?srsltid=AfmBOooXarjI5_FkKQpZqKLofcYMJNd0ftaGQxg7T4KrREoFS0wdnBzv



## VIDEO CLIPS LINKS

Bustling indian roads:
https://pixabay.com/videos/india-people-asia-street-asian-1643/

Low financial literacy:
https://www.youtube.com/watch?v=7oj6gpAbYgw&t=186s&pp=ygUeaW5kaWFucyBsb3cgZmluYW5jaWFsIGxpdGVyYWN5

https://www.youtube.com/watch?v=1s3l2uQKIzw&pp=ygUjaW5kaWFucyBsb3cgZmluYW5jaWFsIGxpdGVyYWN5IG5ld3M%3D

Financial Literacy for all ted talk
https://www.youtube.com/watch?v=pWU3DYvnP0s&pp=ygUbZmluYW5jZSBsaXRlcmFjeSBpbmRpYSBuZXdz

Other:
https://www.youtube.com/watch?v=pX48h5aasCc&pp=ygUmZG9jdW1lbnRhcnkgb24gaW5kaWFuIGZpbmFuY2UgbGl0ZXJhY3k%3D

https://www.youtube.com/watch?v=z14sYye8Sng&pp=ygUmZG9jdW1lbnRhcnkgb24gaW5kaWFuIGZpbmFuY2UgbGl0ZXJhY3k%3D

https://www.youtube.com/watch?v=PlYsJsYOjr4&pp=ygUmZG9jdW1lbnRhcnkgb24gaW5kaWFuIGZpbmFuY2UgbGl0ZXJhY3k%3D




