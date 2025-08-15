import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import json
import os

KEYS_TO_REMOVE = {
    "DFIntRemoteEventSingleInvocationSizeLimit", "FIntUGCValidationLeftArmThresholdFront",
    "FIntUGCValidationRightArmThresholdFront", "FIntUGCValidationRightLegThresholdBack",
    "FIntUGCValidationLeftLegThresholdBack", "FIntUGCValidationHeadAttachmentThreshold",
    "FIntUGCValidationTorsoThresholdBack", "DFIntS2PhysicsSenderRate",
    "DFFlagDebugUseCustomSimHumanoidRadius", "DFIntTouchSenderMaxBandwidthBpsScaling",
    "DFIntTouchSenderMaxBandwidthBps", "FIntUGCValidateLegZMaxSlender",
    "DFIntMaxMissedWorldStepsRemembered", "DFIntGameNetOptimizeParallelPhysicsSendAssemblyBatch",
    "FIntUGCValidationRightLegThresholdSide", "FIntUGCValidationRightLegThresholdFront",
    "FIntUGCValidationTorsoThresholdSide", "FFlagHumanoidParallelFixTickleFloor2",
    "FFlagFixMemoryPriorizationCrash", "FIntUGCValidationTorsoThresholdFront",
    "FIntUGCValidationLeftArmThresholdBack", "FIntUGCValidationLeftArmThresholdSide",
    "FIntUGCValidationLeftLegThresholdFront", "FIntUGCValidationLeftLegThresholdSide",
    "FIntUGCValidationRightArmThresholdBack", "FIntUGCValidationRightArmThresholdSide",
    "DFIntSimAdaptiveHumanoidPDControllerSubstepMultiplier",
    "DFIntPhysicsCountLocalSimulatedTouchEventsHundredthsPercentage", "DFIntDataSenderRate",
    "DFIntMaxClientSimulationRadius", "DFIntSolidFloorPercentForceApplication",
    "DFIntNonSolidFloorPercentForceApplication", "DFIntGameNetPVHeaderTranslationZeroCutoffExponent",
    "FIntParallelDynamicPartsFastClusterBatchSize", "DFIntMaximumFreefallMoveTimeInTenths",
    "DFIntAssemblyExtentsExpansionStudHundredth", "DFIntSimBroadPhasePairCountMax",
    "DFIntPhysicsDecompForceUpgradeVersion", "DFIntMaxAltitudePDStickHipHeightPercent",
    "DFIntUnstickForceAttackInTenths", "DFIntMinClientSimulationRadius",
    "DFIntMinimalSimRadiusBuffer", "DFFlagDebugPhysicsSenderDoesNotShrinkSimRadius",
    "FFlagDebugUseCustomSimRadius", "FIntGameNetLocalSpaceMaxSendIndex",
    "DFFlagSimHumanoidTimestepModelUpdate", "FFlagSimAdaptiveTimesteppingDefault2"
}

class JsonCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Roblox JSON Cleaner")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        self.cleaned_data = None
        self.original_filename = ""

        frame = tk.Frame(root, padx=15, pady=15)
        frame.pack(expand=True, fill=tk.BOTH)

        self.select_button = tk.Button(frame, text="1. Select JSON File", command=self.select_file, height=2)
        self.select_button.pack(fill=tk.X, pady=5)

        self.status_label = tk.Label(frame, text="No file selected.", fg="gray")
        self.status_label.pack(pady=5)

        self.log_area = scrolledtext.ScrolledText(frame, height=15, state='disabled', wrap=tk.WORD, font=("Courier New", 9))
        self.log_area.pack(pady=10, fill=tk.BOTH, expand=True)

        self.save_button = tk.Button(frame, text="2. Save Cleaned File", command=self.save_file, height=2, state='disabled')
        self.save_button.pack(fill=tk.X, pady=5)

    def _update_log(self, message):
        self.log_area.config(state='normal')
        self.log_area.delete('1.0', tk.END)
        self.log_area.insert(tk.END, message)
        self.log_area.config(state='disabled')

    def select_file(self):
        filepath = filedialog.askopenfilename(
            title="Select a JSON file",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        if not filepath: return

        self.original_filename = os.path.basename(filepath)
        self.status_label.config(text=f"File: {self.original_filename}", fg="black")
        self.save_button.config(state='disabled')
        self._update_log("Processing file...")

        try:
            with open(filepath, 'r', encoding='utf-8') as f: data = json.load(f)
            if not isinstance(data, dict):
                self._update_log("Error: The JSON file does not contain an object at its root.")
                return

            self.cleaned_data = {}
            removed_keys = []
            for key, value in data.items():
                if key in KEYS_TO_REMOVE: removed_keys.append(key)
                else: self.cleaned_data[key] = value

            log_message = "✅ Processing complete!\n\n"
            if removed_keys:
                log_message += f"{len(removed_keys)} keys were removed:\n"
                for key in sorted(removed_keys): log_message += f"- {key}\n"
            else:
                log_message += "No keys from the removal list were found in the file."
            
            self._update_log(log_message)
            self.save_button.config(state='normal')

        except json.JSONDecodeError:
            self._update_log(f"Error: The file '{self.original_filename}' is not a valid JSON.")
        except Exception as e:
            self._update_log(f"An unexpected error occurred: {e}")

    def save_file(self):
        if self.cleaned_data is None:
            messagebox.showerror("Error", "No clean data to save.")
            return

        suggested_filename = f"cleaned_{self.original_filename}"
        filepath = filedialog.asksaveasfilename(
            title="Save cleaned file as...",
            initialfile=suggested_filename,
            defaultextension=".json",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        if not filepath: return
            
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.cleaned_data, f, indent=4)
            messagebox.showinfo("Success", "The cleaned file was saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save the file.\nDetails: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JsonCleanerApp(root)
    root.mainloop()