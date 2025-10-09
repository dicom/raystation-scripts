# Forces all clinical goals to be associated with the plan.
#
# Authors:
# Robert Hoggard
# Helse Møre og Romsdal HF
#

# Import RS resources
from connect import *

import tkinter as tk
from tkinter import messagebox

# Get the current patient, case, and plan dynamically
patient = get_current("Patient")
case = get_current("Case")
plan = get_current("Plan")

# Ensure all objects are retrieved successfully
if not patient or not case or not plan:
    raise ValueError("Error: Could not retrieve the current patient, case, or plan.")

# Retrieve the evaluation setup
evaluation_setup = plan.TreatmentCourse.EvaluationSetup

# Track statistics
converted_count = 0
skipped_count = 0

# Function to check if a similar clinical goal already exists (without beam set association)
def goal_exists(planning_goal):
    for existing_goal in evaluation_setup.EvaluationFunctions:
        if hasattr(existing_goal, "PlanningGoal") and existing_goal.PlanningGoal:
            existing = existing_goal.PlanningGoal
            if (
                existing.Type == planning_goal.Type and
                existing.GoalCriteria == planning_goal.GoalCriteria and
                existing.PrimaryAcceptanceLevel == planning_goal.PrimaryAcceptanceLevel and
                existing.SecondaryAcceptanceLevel == planning_goal.SecondaryAcceptanceLevel and
                existing.ParameterValue == planning_goal.ParameterValue and
                existing.IsComparativeGoal == planning_goal.IsComparativeGoal and
                existing.Priority == planning_goal.Priority and
                not hasattr(existing_goal, "OfDoseDistributions")  # Ensure it's plan-associated
            ):
                return True  # Identical goal already exists
    return False

# Iterate through all clinical goals
for function in evaluation_setup.EvaluationFunctions:
    if hasattr(function, "PlanningGoal") and function.PlanningGoal:
        planning_goal = function.PlanningGoal

        # Check if the clinical goal is associated with a beam set
        if hasattr(function, "OfDoseDistributions") and function.OfDoseDistributions:
            for dose_distribution in function.OfDoseDistributions:
                if hasattr(dose_distribution, "ForBeamSet") and dose_distribution.ForBeamSet:
                    
                    # Check if an identical clinical goal (without beam set) already exists
                    if goal_exists(planning_goal):
                        skipped_count += 1
                        print(f"Skipped duplicate goal for ROI '{function.ForRegionOfInterest.Name if function.ForRegionOfInterest else 'Unknown'}'")
                        continue  # Skip processing this goal
                    
                    # Extract relevant parameters from PlanningGoal
                    roi_name = function.ForRegionOfInterest.Name if function.ForRegionOfInterest else None
                    goal_criteria = planning_goal.GoalCriteria
                    goal_type = planning_goal.Type
                    primary_acceptance_level = planning_goal.PrimaryAcceptanceLevel
                    secondary_acceptance_level = planning_goal.SecondaryAcceptanceLevel
                    parameter_value = planning_goal.ParameterValue
                    is_comparative_goal = planning_goal.IsComparativeGoal
                    priority = planning_goal.Priority

                    # Try to edit the clinical goal
                    try:
                        evaluation_setup.EditClinicalGoal(
                            FunctionToEdit=function,
                            RoiName=roi_name,
                            GoalCriteria=goal_criteria,
                            GoalType=goal_type,
                            PrimaryAcceptanceLevel=primary_acceptance_level,
                            SecondaryAcceptanceLevel=secondary_acceptance_level,
                            ParameterValue=parameter_value,
                            IsComparativeGoal=is_comparative_goal,
                            BeamSet=None,  # Remove beam set association
                            Priority=priority,
                            AssociateToPlan=True  # Ensure the goal is now associated with the plan
                        )

                        converted_count += 1
                        print(f"Converted clinical goal for ROI '{roi_name}' to be associated with the plan instead of a beam set.")

                    except Exception as e:
                        skipped_count += 1
                        print(f"Error updating clinical goal for ROI '{roi_name}': {e}")

# Create a summary message with taskbar presence
summary_title = "Plan Quality Control"
summary_text = (
    f"Successfully converted {converted_count} clinical goals.\n"
    f"Skipped {skipped_count} duplicate goals.\n"
)

# Create and configure the Tkinter window for taskbar presence
root = tk.Tk()  # Create the root window
root.withdraw()  # Hide the root window (prevents it from flashing)
root.deiconify()  # Show the root window (so it has a taskbar presence)
root.title(summary_title)  # Set the window title

# Show message box
messagebox.showinfo(summary_title, summary_text)

# Close the Tkinter window after the messagebox is dismissed
root.destroy()

print("All clinical goals with beam set associations have been processed.")
