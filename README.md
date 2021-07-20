# qm_project
Bicycle project crowd evaluation.

This repository is created for evaluating the quality and performance of a new crowd in the project Bicycle crowd evaluation.  

The directory 'main_scripts' contains the scripts used for different analyzing purposes:

* Task 1:
    * task_1a.py
         * analyze the annotators contributing to the dataset and create the *'annotators.csv'*.
    * task_1b.py
         * analyze the annotation time and create the *'annotation_time.csv'*.
    * task_1b_by_image.py
         * analyze annotation time grouped by images and create the *'annotation_time_by_image.csv'*.
    * task_1b_by_user.py
         * analyze annotation time grouped by users and create the *'annotation_time_by_user.csv'*.
    * task_1c.py
         * analyze the amount of results of each annotator and create the *'annotator_result_count.csv'*.
    * task_1d.py
         * analyze the  highly disagree questions and create the *'question_answers.csv'*, *'question_groups.csv'* and *'highly_disagree_group.csv'*.

* Task 2:
    * task_2.py
         * analyze the occurrence of samples with label 'cant_solve' and 'corrupt_data' marked as True, and create the *'grouped_unsolved_data.csv'*
* Task 3:
    * task_3.py
         * analyze the balance of the reference set
* Task 4:
    * task_4_export.py
         * collect data by doing cross-checking all answers with the reference set. The execution takes approximately 45 minutes to complete and it only needs to execute once to create the *'annotators_quality_assessment.csv'* file.
    * task_4_visualization.py
         * visualize and analyze the answers of all annotators
    * task_4_visualization_extra.py
         * visualize and analyze the answers of annotators with sample sizes greater than the standard deviation limit.
    * task_4_good_bad_annotators.py
         * Produce the data of a group of chosen annotators
 

The directory 'files' contains the csv files created from the .py files  

