/**
 * Data Processor for FTSE 100 Historical Analysis
 * Processes CSV data and calculates all risk analysis metrics
 */

const fs = require('fs');

class DataProcessor {
    constructor() {
        this.rawData = [];
        this.processedData = {
            metadata: {
                totalRecords: 0,
                dateRange: {
                    start: null,
                    end: null
                },
                currentValue: 0,
                processedDate: new Date().toISOString()
            },
            yearlyData: [],
            riskAnalysis: {
                periods: [10, 20, 30, 40],
                results: []
            }
        };
    }

    /**
     * Load and parse CSV file
     */
    loadCSV(filePath) {
        try {
            const csvContent = fs.readFileSync(filePath, 'utf8');
            const lines = csvContent.split('\n');
            
            // Skip header row
            for (let i = 1; i < lines.length; i++) {
                const row = lines[i].split(',');
                if (row.length >= 5 && row[0].trim()) {
                    this.rawData.push({
                        date: row[0].trim(),
                        open: parseFloat(row[1]),
                        high: parseFloat(row[2]),
                        low: parseFloat(row[3]),
                        close: parseFloat(row[4])
                    });
                }
            }
            
            // Sort by date
            this.rawData.sort((a, b) => new Date(a.date) - new Date(b.date));
            
            // Update metadata
            this.processedData.metadata.totalRecords = this.rawData.length;
            this.processedData.metadata.dateRange.start = this.rawData[0].date;
            this.processedData.metadata.dateRange.end = this.rawData[this.rawData.length - 1].date;
            this.processedData.metadata.currentValue = this.rawData[this.rawData.length - 1].close;
            
            console.log(`Loaded ${this.rawData.length} records`);
            console.log(`Date range: ${this.processedData.metadata.dateRange.start} to ${this.processedData.metadata.dateRange.end}`);
            
        } catch (error) {
            console.error('Error loading CSV:', error);
            throw error;
        }
    }

    /**
     * Calculate yearly growth rates
     */
    calculateYearlyGrowth() {
        const yearlyData = {};
        
        // Group data by year
        this.rawData.forEach(record => {
            const year = new Date(record.date).getFullYear();
            if (!yearlyData[year]) {
                yearlyData[year] = [];
            }
            yearlyData[year].push(record);
        });
        
        // Calculate yearly growth
        const years = Object.keys(yearlyData).sort((a, b) => parseInt(a) - parseInt(b));
        
        years.forEach((year, index) => {
            const yearData = yearlyData[year];
            const startValue = yearData[0].close;
            const endValue = yearData[yearData.length - 1].close;
            const growth = ((endValue - startValue) / startValue) * 100;
            
            this.processedData.yearlyData.push({
                year: parseInt(year),
                startValue: startValue,
                endValue: endValue,
                growth: growth,
                recordCount: yearData.length
            });
        });
        
        console.log(`Calculated yearly growth for ${this.processedData.yearlyData.length} years`);
    }

    /**
     * Calculate average annual growth for a specific period
     */
    calculateAverageGrowthForPeriod(years) {
        const endYear = new Date(this.processedData.metadata.dateRange.end).getFullYear();
        const startYear = endYear - years + 1;
        
        const periodData = this.processedData.yearlyData.filter(
            year => year.year >= startYear && year.year <= endYear
        );
        
        if (periodData.length === 0) return null;
        
        const totalGrowth = periodData.reduce((sum, year) => sum + year.growth, 0);
        const averageGrowth = totalGrowth / periodData.length;
        
        return {
            period: years,
            startYear: startYear,
            endYear: endYear,
            yearsIncluded: periodData.length,
            averageGrowth: averageGrowth,
            yearlyGrowths: periodData.map(y => ({ year: y.year, growth: y.growth }))
        };
    }

    /**
     * Get value from X years ago
     */
    getValueFromYearsAgo(years) {
        const currentDate = new Date(this.processedData.metadata.dateRange.end);
        const targetDate = new Date(currentDate.getTime() - (years * 365.25 * 24 * 60 * 60 * 1000));
        
        // Find closest record to target date
        let closestRecord = this.rawData[0];
        let closestDiff = Math.abs(new Date(this.rawData[0].date) - targetDate);
        
        for (let i = 1; i < this.rawData.length; i++) {
            const diff = Math.abs(new Date(this.rawData[i].date) - targetDate);
            if (diff < closestDiff) {
                closestDiff = diff;
                closestRecord = this.rawData[i];
            }
        }
        
        return closestRecord;
    }

    /**
     * Calculate years between two dates
     */
    calculateYears(startDate, endDate) {
        const start = new Date(startDate);
        const end = new Date(endDate);
        return (end - start) / (1000 * 60 * 60 * 24 * 365.25);
    }

    /**
     * Calculate risk analysis for all periods
     */
    calculateRiskAnalysis() {
        const currentValue = this.processedData.metadata.currentValue;
        const periods = this.processedData.riskAnalysis.periods;
        
        periods.forEach(period => {
            // Get average growth for this period
            const periodAnalysis = this.calculateAverageGrowthForPeriod(period);
            
            if (periodAnalysis) {
                // Get starting value from X years ago
                const startRecord = this.getValueFromYearsAgo(period);
                const actualYears = this.calculateYears(startRecord.date, this.processedData.metadata.dateRange.end);
                
                // Calculate expected value
                const expectedValue = startRecord.close * Math.pow(1 + (periodAnalysis.averageGrowth / 100), actualYears);
                
                // Calculate deviation
                const deviation = ((currentValue - expectedValue) / expectedValue) * 100;
                
                this.processedData.riskAnalysis.results.push({
                    period: period,
                    startDate: startRecord.date,
                    startValue: startRecord.close,
                    currentValue: currentValue,
                    expectedValue: expectedValue,
                    averageGrowth: periodAnalysis.averageGrowth,
                    actualYears: actualYears,
                    deviation: deviation,
                    yearsIncluded: periodAnalysis.yearsIncluded,
                    yearlyGrowths: periodAnalysis.yearlyGrowths
                });
            }
        });
        
        console.log(`Calculated risk analysis for ${this.processedData.riskAnalysis.results.length} periods`);
    }

    /**
     * Process all data
     */
    process() {
        console.log('Starting data processing...');
        this.calculateYearlyGrowth();
        this.calculateRiskAnalysis();
        console.log('Data processing complete');
    }

    /**
     * Save processed data to JSON file
     */
    saveToJSON(filePath) {
        try {
            const jsonData = JSON.stringify(this.processedData, null, 2);
            fs.writeFileSync(filePath, jsonData);
            console.log(`Processed data saved to ${filePath}`);
        } catch (error) {
            console.error('Error saving JSON:', error);
            throw error;
        }
    }

    /**
     * Display summary
     */
    displaySummary() {
        console.log('\n=== PROCESSING SUMMARY ===');
        console.log(`Total records: ${this.processedData.metadata.totalRecords}`);
        console.log(`Date range: ${this.processedData.metadata.dateRange.start} to ${this.processedData.metadata.dateRange.end}`);
        console.log(`Current value: ${this.processedData.metadata.currentValue}`);
        console.log(`Years of data: ${this.processedData.yearlyData.length}`);
        
        console.log('\n=== RISK ANALYSIS ===');
        this.processedData.riskAnalysis.results.forEach(result => {
            console.log(`${result.period} years: Start=${result.startValue.toFixed(2)}, Expected=${result.expectedValue.toFixed(2)}, Current=${result.currentValue.toFixed(2)}, Deviation=${result.deviation.toFixed(2)}%`);
        });
    }
}

// Main execution
if (require.main === module) {
    const processor = new DataProcessor();
    
    try {
        processor.loadCSV('./ftse100.csv');
        processor.process();
        processor.saveToJSON('./ftse100-analysis.json');
        processor.displaySummary();
    } catch (error) {
        console.error('Processing failed:', error);
    }
}

module.exports = DataProcessor;