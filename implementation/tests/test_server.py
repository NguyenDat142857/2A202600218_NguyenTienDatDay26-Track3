#!/usr/bin/env python3
"""
Unit tests for SQLite Lab MCP Server.
"""

import unittest
import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from db import SQLiteAdapter, ValidationError
from init_db import create_database


class TestSQLiteAdapter(unittest.TestCase):
    """Test cases for SQLiteAdapter."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database once for all tests."""
        cls.db_path = "test_unit.db"
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
        create_database(cls.db_path)
        cls.adapter = SQLiteAdapter(cls.db_path)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test database."""
        cls.adapter.close()
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
    
    def test_list_tables(self):
        """Test listing tables."""
        tables = self.adapter.list_tables()
        self.assertIn('students', tables)
        self.assertIn('courses', tables)
        self.assertIn('enrollments', tables)
    
    def test_get_table_schema(self):
        """Test getting table schema."""
        schema = self.adapter.get_table_schema('students')
        self.assertIsInstance(schema, list)
        self.assertGreater(len(schema), 0)
        
        # Check column structure
        column_names = [col['name'] for col in schema]
        self.assertIn('id', column_names)
        self.assertIn('name', column_names)
        self.assertIn('cohort', column_names)
    
    def test_search_basic(self):
        """Test basic search."""
        result = self.adapter.search('students')
        self.assertIn('rows', result)
        self.assertIn('count', result)
        self.assertGreater(result['count'], 0)
    
    def test_search_with_filters(self):
        """Test search with filters."""
        result = self.adapter.search(
            'students',
            filters=[{"column": "cohort", "operator": "eq", "value": "A1"}]
        )
        self.assertGreater(result['count'], 0)
        for row in result['rows']:
            self.assertEqual(row['cohort'], 'A1')
    
    def test_search_with_ordering(self):
        """Test search with ordering."""
        result = self.adapter.search(
            'students',
            order_by='score',
            descending=True,
            limit=2
        )
        self.assertEqual(len(result['rows']), 2)
        # Check descending order
        if len(result['rows']) == 2:
            self.assertGreaterEqual(result['rows'][0]['score'], result['rows'][1]['score'])
    
    def test_search_with_pagination(self):
        """Test search with pagination."""
        result1 = self.adapter.search('students', limit=2, offset=0)
        result2 = self.adapter.search('students', limit=2, offset=2)
        
        self.assertEqual(len(result1['rows']), 2)
        self.assertEqual(len(result2['rows']), 2)
        # Ensure different results
        self.assertNotEqual(result1['rows'][0]['id'], result2['rows'][0]['id'])
    
    def test_insert(self):
        """Test insert operation."""
        result = self.adapter.insert(
            'students',
            {
                'name': 'Unit Test Student',
                'cohort': 'TEST',
                'email': 'unittest@example.com',
                'score': 100.0
            }
        )
        self.assertIn('id', result)
        self.assertEqual(result['name'], 'Unit Test Student')
    
    def test_aggregate_count(self):
        """Test count aggregate."""
        result = self.adapter.aggregate('students', 'count')
        self.assertEqual(len(result), 1)
        self.assertIn('value', result[0])
        self.assertGreater(result[0]['value'], 0)
    
    def test_aggregate_avg(self):
        """Test average aggregate."""
        result = self.adapter.aggregate('students', 'avg', column='score')
        self.assertEqual(len(result), 1)
        self.assertIn('value', result[0])
        self.assertIsInstance(result[0]['value'], (int, float))
    
    def test_aggregate_with_group_by(self):
        """Test aggregate with group by."""
        result = self.adapter.aggregate(
            'students',
            'count',
            group_by='cohort'
        )
        self.assertGreater(len(result), 0)
        for row in result:
            self.assertIn('cohort', row)
            self.assertIn('value', row)
    
    def test_invalid_table(self):
        """Test invalid table name."""
        with self.assertRaises(ValidationError):
            self.adapter.search('invalid_table')
    
    def test_invalid_column(self):
        """Test invalid column name."""
        with self.assertRaises(ValidationError):
            self.adapter.search('students', columns=['invalid_column'])
    
    def test_invalid_operator(self):
        """Test invalid filter operator."""
        with self.assertRaises(ValidationError):
            self.adapter.search(
                'students',
                filters=[{"column": "name", "operator": "invalid", "value": "test"}]
            )
    
    def test_invalid_metric(self):
        """Test invalid aggregate metric."""
        with self.assertRaises(ValidationError):
            self.adapter.aggregate('students', 'invalid_metric')
    
    def test_empty_insert(self):
        """Test empty insert values."""
        with self.assertRaises(ValidationError):
            self.adapter.insert('students', {})
    
    def test_filter_operators(self):
        """Test various filter operators."""
        # Test gt operator
        result = self.adapter.search(
            'students',
            filters=[{"column": "score", "operator": "gt", "value": 90}]
        )
        for row in result['rows']:
            self.assertGreater(row['score'], 90)
        
        # Test like operator
        result = self.adapter.search(
            'students',
            filters=[{"column": "name", "operator": "like", "value": "%Van%"}]
        )
        for row in result['rows']:
            self.assertIn('Van', row['name'])
    
    def test_aggregate_functions(self):
        """Test all aggregate functions."""
        # Test sum
        result = self.adapter.aggregate('students', 'sum', column='score')
        self.assertGreater(result[0]['value'], 0)
        
        # Test min
        result = self.adapter.aggregate('students', 'min', column='score')
        self.assertIsNotNone(result[0]['value'])
        
        # Test max
        result = self.adapter.aggregate('students', 'max', column='score')
        self.assertIsNotNone(result[0]['value'])


if __name__ == '__main__':
    unittest.main()
