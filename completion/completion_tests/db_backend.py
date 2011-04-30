from completion.backends.db_backend import DatabaseAutocomplete
from completion.completion_tests.base import AutocompleteTestCase, AutocompleteBackendTestCase
from completion.completion_tests.models import Blog, Note1, Note2, Note3, BlogProvider, NoteProvider
from completion.models import AutocompleteObject
from completion.sites import AutocompleteSite


test_site = AutocompleteSite(DatabaseAutocomplete())
test_site.register(Blog, BlogProvider)
test_site.register(Note1, NoteProvider)
test_site.register(Note2, NoteProvider)
test_site.register(Note3, NoteProvider)


class DatabaseBackendTestCase(AutocompleteTestCase, AutocompleteBackendTestCase):
    def setUp(self):
        self.test_site = test_site
        AutocompleteTestCase.setUp(self)
        test_site.flush()
    
    def test_storing_providers(self):
        self.assertEqual(AutocompleteObject.objects.count(), 0)
        
        test_site.store_providers()
        self.assertEqual(AutocompleteObject.objects.count(), 6)
        
        titles = AutocompleteObject.objects.values_list('title', flat=True)
        self.assertEqual(sorted(titles), [
            'testingpython',
            'testingpythoncode',
            'testingpythoncode',
            'testswithpython',
            'unittestswith',
            'webtestingpython'
        ])
    
    def test_storing_objects_db(self):
        test_site.store_object(self.blog_tp)
        self.assertEqual(AutocompleteObject.objects.count(), 1)
        
        test_site.store_object(self.blog_tpc)
        self.assertEqual(AutocompleteObject.objects.count(), 2)
        
        test_site.store_object(self.blog_tp) # storing again does not produce dupe
        self.assertEqual(AutocompleteObject.objects.count(), 2)
        
        test_site.store_object(self.blog_wtp)
        self.assertEqual(AutocompleteObject.objects.count(), 4)
    
    def test_removing_objects_db(self):
        test_site.store_providers()
        
        test_site.remove_object(self.blog_tp)
        self.assertEqual(AutocompleteObject.objects.count(), 5)
        
        test_site.remove_object(self.blog_tp)
        self.assertEqual(AutocompleteObject.objects.count(), 5)
        
        test_site.remove_object(self.blog_tpc)
        self.assertEqual(AutocompleteObject.objects.count(), 4)
