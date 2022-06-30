Project made under Microsoft Engage Mentorship Program 2022
- [PPT](https://www.canva.com/design/DAFB_cm8eMI/Q7YVr2-E_QvsalaPEe6LqA/view?utm_content=DAFB_cm8eMI&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink)
- [Demo video](https://drive.google.com/file/d/1f0OFYAVQipJB_dWWoaDHANjYGjbutffW/view?usp=sharing)

# FindingMissingPeople_FaceRecognition
A website to help police to find lost persons and unite them with their families using Face Recognition technology

## Installation and Setup guide
After cloning this repository in your local machine follow the given steps to be able to run the code:

1. Create and activate a virtual enviornment in the same directory. (Optional but recommended)
2. Download and Install [Microsoft Visual Studio](https://visualstudio.microsoft.com/).
3. While insatlling don't forget to click on **Desktop development with c++** option as shown [here](https://docs.microsoft.com/en-us/cpp/build/media/vscpp-concierge-choose-workload.gif?view=msvc-170).
4. Install all the dependencies mentioned in *requirements.txt* file using command: ```pip install -r requirements.txt``` in cmd/terminal.
5. Start *phpmyadmin* and create a new mysql database with name **finding_missing_people**
6. Import [finding_missing_people.sql](https://github.com/1218muskan/FindingMissingPeople_FaceRecognition/blob/main/finding_missing_people.sql) file to the database to create the tables.
7. Run main.py file
8. Open the website from local host: http://127.0.0.1:5000/

If facing issues in Step 4 while installing *dlib library* on windows 10 refer to [this article](https://medium.com/analytics-vidhya/how-to-install-dlib-library-for-python-in-windows-10-57348ba1117f).
