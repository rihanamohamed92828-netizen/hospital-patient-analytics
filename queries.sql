-- name: kpis
SELECT COUNT(*) AS admissions,
       ROUND(AVG(length_of_stay),1) AS avg_length_of_stay,
       ROUND(AVG(billing_amount),0) AS avg_bill,
       ROUND(SUM(billing_amount)/1e6,1) AS total_billing_millions
FROM admissions;
-- name: by_condition
SELECT medical_condition, COUNT(*) AS admissions,
       ROUND(AVG(length_of_stay),1) AS avg_los, ROUND(AVG(billing_amount),0) AS avg_bill
FROM admissions GROUP BY medical_condition ORDER BY admissions DESC;
-- name: by_admission_type
SELECT admission_type, COUNT(*) AS admissions, ROUND(AVG(billing_amount),0) AS avg_bill,
       ROUND(AVG(length_of_stay),1) AS avg_los
FROM admissions GROUP BY admission_type ORDER BY admissions DESC;
-- name: by_age_group
SELECT age_group, COUNT(*) AS admissions, ROUND(AVG(billing_amount),0) AS avg_bill
FROM admissions GROUP BY age_group ORDER BY age_group;
-- name: by_insurer
SELECT insurance_provider, COUNT(*) AS admissions, ROUND(SUM(billing_amount)/1e6,1) AS billing_millions
FROM admissions GROUP BY insurance_provider ORDER BY billing_millions DESC;
-- name: monthly
SELECT substr(date_of_admission,1,7) AS month, COUNT(*) AS admissions
FROM admissions GROUP BY month ORDER BY month;
-- name: test_results
SELECT medical_condition, test_results, COUNT(*) AS n
FROM admissions GROUP BY medical_condition, test_results ORDER BY medical_condition, n DESC;
-- name: top_doctors
SELECT doctor, COUNT(*) AS admissions, ROUND(AVG(length_of_stay),1) AS avg_los
FROM admissions GROUP BY doctor HAVING COUNT(*) >= 5 ORDER BY admissions DESC LIMIT 10;
