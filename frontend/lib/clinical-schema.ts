
export interface ClinicalField {
  name: string;
  label: string;
  description: string;
  type: "number" | "select";
  options?: { label: string; value: string }[];
  min?: number;
  max?: number;
  step?: number;
}

export const clinicalFields: ClinicalField[] = [
  {
    name: "age",
    label: "Age",
    description: "Age in years",
    type: "number",
    min: 1,
    max: 120,
  },
  {
    name: "sex",
    label: "Sex",
    description: "Dataset encoding: 1 = male, 0 = female",
    type: "select",
    options: [
      { label: "Male (1)", value: "1" },
      { label: "Female (0)", value: "0" },
    ],
  },
  {
    name: "cp",
    label: "Chest Pain Type",
    description: "Clinical chest pain category",
    type: "select",
    options: [
      { label: "Typical angina (1)", value: "1" },
      { label: "Atypical angina (2)", value: "2" },
      { label: "Non-anginal pain (3)", value: "3" },
      { label: "Asymptomatic (4)", value: "4" },
    ],
  },
  {
    name: "trestbps",
    label: "Resting Blood Pressure",
    description: "Resting systolic blood pressure in mmHg",
    type: "number",
    min: 50,
    max: 250,
  },
  {
    name: "chol",
    label: "Serum Cholesterol",
    description: "Serum cholesterol in mg/dL",
    type: "number",
    min: 0,
    max: 700,
  },
  {
    name: "fbs",
    label: "Fasting Blood Sugar",
    description: "Whether fasting blood sugar is greater than 120 mg/dL",
    type: "select",
    options: [
      { label: "No (0)", value: "0" },
      { label: "Yes (1)", value: "1" },
    ],
  },
  {
    name: "restecg",
    label: "Resting ECG",
    description: "Resting electrocardiographic result",
    type: "select",
    options: [
      { label: "Normal (0)", value: "0" },
      { label: "ST-T abnormality (1)", value: "1" },
      { label: "LV hypertrophy (2)", value: "2" },
    ],
  },
  {
    name: "thalach",
    label: "Maximum Heart Rate",
    description: "Maximum heart rate achieved",
    type: "number",
    min: 50,
    max: 250,
  },
  {
    name: "exang",
    label: "Exercise-Induced Angina",
    description: "Angina induced by exercise",
    type: "select",
    options: [
      { label: "No (0)", value: "0" },
      { label: "Yes (1)", value: "1" },
    ],
  },
  {
    name: "oldpeak",
    label: "Oldpeak",
    description: "ST depression induced by exercise relative to rest",
    type: "number",
    min: 0,
    max: 10,
    step: 0.1,
  },
  {
    name: "slope",
    label: "ST Segment Slope",
    description: "Slope of the peak exercise ST segment",
    type: "select",
    options: [
      { label: "Upsloping (1)", value: "1" },
      { label: "Flat (2)", value: "2" },
      { label: "Downsloping (3)", value: "3" },
    ],
  },
  {
    name: "ca",
    label: "Major Vessels",
    description: "Number of major vessels: 0–3",
    type: "select",
    options: [
      { label: "0", value: "0" },
      { label: "1", value: "1" },
      { label: "2", value: "2" },
      { label: "3", value: "3" },
    ],
  },
  {
    name: "thal",
    label: "Thalassemia Category",
    description: "Legacy Cleveland dataset encoding",
    type: "select",
    options: [
      { label: "Normal (3)", value: "3" },
      { label: "Fixed defect (6)", value: "6" },
      { label: "Reversible defect (7)", value: "7" },
    ],
  },
];
